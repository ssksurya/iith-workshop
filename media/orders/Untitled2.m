clc
close all 
clear all
syms   a A x y l b t d  v m
w =  a*sin(m*pi*x/l)*(sin(pi*y/b))^2;
temp1 = diff(diff(w,x),x);
temp2 = diff(diff(w,y),y);
temp3 = diff(diff(w,y),x);
temp4 = diff(w,x);
f1 = 0.5*((d*((temp1+temp2)^2-(2*(1-v)*(temp1*temp2)-temp3^2)))- (A*t*(temp4)^2));
f2 = int(f1,x,0,l);
assume(m,'integer');
f3 = simplify(f2);
f4 = int(f3,y,0,b);
assume(m,'integer');
f5 = simplify(f4);
f6 = diff(f5,a);
b = 1;
l = 2*b;
t = 0.0001;
v = 0.3;
E = 2700000;
d = E*t^3/(12*(1-v^2));
a = 1;
f7 = solve(f6,A);
f8 = subs(f7);
f9 = diff(f8,m);
out=simplify(f9);
[num,den]=numden(out);
coeffs=sym2poly(num);
myroots=roots(coeffs);
real_roots = real(myroots);
a = 1;
for i = 1:length(real_roots)
    if(real_roots(i) > 1e-4)
        m = real_roots(i);
        ans(a) = double(simplify(subs(f8)));
        a = a+1;
    end
end

    



