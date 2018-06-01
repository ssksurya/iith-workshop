 hold on;   
 clc;
 clear all;
 
Xl=0;Xu=10;Yl=0;Yu=10; % area of material to be deposited
X = [0;1;1;0;0];       % x,y,z coordinates 
 Y = [0;0;1;1;0];
 Z = [0;0;0;0;0];
 dY = [1;1;1;1;1];     % increments 
 dX = [1;1;1;1;1];
 t=0; t1=0.05; % each block deposition
 a=0;b=0;c=0;d=0;P=[]; e=0;A=[];B=[];T=[];
 eff=0.7; ff=0.6;V=240;I=5;af=3;ba=5;ca=4;
Q = eff*V*I;
Nr= 6*sqrt(3)*Q*ff;
Dr= pi*sqrt(pi)*af*ba*ca;
const = Nr/Dr;
for j=0:1:Yu/2-1
       for i=0:1:Xu-1     % L==>R loop
         if i>=j
              
           X1= X+(i)*dX;
         if (Xu-X1)>j
         plot3(X1,Y,Z);   % draw a square in the xy plane with z = 0
         plot3(X1,Y,Z+1); % draw a square in the xy plane with z = 1
         set(gca,'View',[-28,35]); % set the azimuth and elevation of the plot  
            for k=1:length(X)-1
                figure(1)
                 plot3([X1(k);X1(k)],[Y(k);Y(k)],[0;1]);
                 axis equal;     
            end
     pause(t1)
     t=t+t1
     a=a+1;
     Xa= min(X1)+0.5;
     Ya= min(Y)+0.5;
     Za= min(Z)+0.5;
     P(a,:)= [ Xa Ya Za t];
     e=e+1;
             end
         end
       end
    X1=X+(i-j)*dX;
    for l =0:1:Yu-j-1       % B==>T loop
         
        Y1= Y+l*dY;
        if Y1<Yu-j
        plot3(X1,Y1,Z);
        plot3(X1,Y1,Z+1);
            for k=1:length(Y)-1
                figure(1)
                 plot3([X1(k);X1(k)],[Y1(k);Y1(k)],[0;1]);
                 axis equal;     
            end 
            pause(t1)
            t=t+t1    % time of deposition
        a=a+1;
     Xa= min(X1)+0.5;
     Ya= min(Y1)+0.5;
     Za= min(Z)+0.5;
     P(a,:)= [ Xa Ya Za t];
     e=e+1;
        end
    end
    Y1=Y1-j*dY;
 for l =0:1:Xu-j-1       % R==>L loop
        X2 = X1-l;
        if X2>=j
        plot3(X2,Y1,Z);
        plot3(X2,Y1,Z+1);
            for k=1:length(X)-1
                figure(1)
                 plot3([X2(k);X2(k)],[Y1(k);Y1(k)],[0;1]);
                 axis equal;     
            end 
            pause(t1)
            t=t+t1    % time of deposition
        a=a+1;
     Xa= min(X2)+0.5;
     Ya= min(Y1)+0.5;
     Za= min(Z)+0.5;
     P(a,:)= [ Xa Ya Za t];
     e=e+1;
        end 
 end
 X2=X2+j*dX;
   for l =0:1:Yu-j-2       % T==>B loop
        Y1= Y1-dY;
         if Y1>j
        plot3(X2,Y1,Z);
        plot3(X2,Y1,Z+1);
            for k=1:length(Y)-1
                figure(1)
                 plot3([X2(k);X2(k)],[Y1(k);Y1(k)],[0;1]);
                 axis equal;     
            end 
            pause(t1)
            t=t+t1    % time of deposition
         a=a+1;
     Xa= min(X2)+0.5;
     Ya= min(Y1)+0.5;
     Za= min(Z)+0.5;
     P(a,:)= [ Xa Ya Za t];
     e=e+1;
         end 
   end 
   Y=Y+dY;
end
R = P(:,1:3);
M= zeros(e*e,1);
for i=1:1:e
   A(((e*(i-1)+1):e*i),:)= [R(:,1:3) ] ;
   B(((e*(i-1)+1):e*i),:) = t1*i;
   mat = [(e*(i-1)+1):(e*(i-1)+i)];
   M(mat) = 1;
end
C=[A B M]; %A=coordinates,B= time instance, C= material condition
Px=A(:,1); Py = A(:,2); Pz=A(:,3);
 
for i = 1:1:e
    for j = (e*(i-1)+1):1:e*i
         
        if M(j)==1
            if max(abs(Px(e*(i-1)+i)-Px(j)),(abs(Py(e*(i-1)+i)-Py(j))))== 0
                T(j)=1150;
            elseif max(abs(Px(e*(i-1)+i)-Px(j)),(abs(Py(e*(i-1)+i)-Py(j))))== 1
                T(j)=950;
            elseif max(abs(Px(e*(i-1)+i)-Px(j)),(abs(Py(e*(i-1)+i)-Py(j))))== 2
                T(j)=750;
            elseif max(abs(Px(e*(i-1)+i)-Px(j)),(abs(Py(e*(i-1)+i)-Py(j))))== 3
                T(j)=550;
            elseif max(abs(Px(e*(i-1)+i)-Px(j)),(abs(Py(e*(i-1)+i)-Py(j))))== 4
                T(j)=350;
            else
                T(j)=300;
            end
            qf(j) = const*exp(-3*(((Px(e*(i-1)+i)-Px(j))^2)/af^2+((Py(e*(i-1)+i)-Py(j))^2)/ba^2));
        end
    end
end
 
D=[ A B M T']; % 0 in column indicates no material
 
for i = 1:1:e
    P1x(i,:)=Px((e*(e-1)+i));  % last block filling instance temperature
    P1y(i,:)=Py((e*(e-1)+i));
    T1(i,:) =T((e*(e-1)+i)) ;
    q1f(i,:)=qf((e*(e-1)+i));
end
 
figure(2);
plot3 (P1x,P1y,T1);
title('Temperature plot line');
figure(3)
plot3(P1x,P1y,q1f,'r');
title('heat distribution plot line');
Xs=[];Ys=[];Ts=[];Qfs=[];r=0;s=0;
for i=1:1:(Xu-Xl)
    s=0;
    for j=1:1:(Yu-Yl)
     Ppx(10*(i-1)+j,:)= 0.5+s;
     Ppy(10*(i-1)+j,:)= 0.5+r;
     s=s+1; 
    end 
    r=r+1;
end
for i=1:1:(Xu-Xl)*(Yu-Yl)
    for j=1:1:(Xu-Xl)*(Xu-Xl)
        if (Ppx(i)== P1x(j))&&(Ppy(i)==P1y(j))
            Tp(i,:)= T1(j);
            qp(i,:)= q1f(j);
        end     
    end
end
for i=1:1:(sqrt(e))
    for j=1:1:(sqrt(e))
       Ts(i,j)= Tp((10*(i-1)+j));
        qs(i,j)= qp((10*(i-1)+j));

        end
end
 
[XX YY]= meshgrid(Xl+0.5:1:Xu-0.5,Yl+0.5:1:Yu-0.5);
figure(4)
surf(XX,YY,Ts,'FaceColor','interp','EdgeColor','k');
title('temperature surface plot');
figure(5)
surf(XX,YY,qs,'FaceColor','interp','EdgeColor','k');
title('heat distribution surface plot');
figure(6)
bar3(Ts,0.8);
title('temperature bar plot');
axis tight;
figure(7)
bar3(qs,0.8);
title('heat distribution bar plot');
axis tight;