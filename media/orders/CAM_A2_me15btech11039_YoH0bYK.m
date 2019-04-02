
clc
clear
close all

% Image to G_Code


Image=imread('input.jpg');
Image1=rgb2gray(Image);
Image2= (Image1);
fid = fopen('G_code.txt','wt+');
p1 = [0 0 0];
fprintf(fid,'G90 G00 X%f Y%f Z%f \r\n', p1);

for i=1:size(Image2,1)-1
    for j=1:size(Image2,2)-1
       p = [i     j    (255-Image2(i,j))/20.0 ];
       if ~(isnan(p1))
		    fprintf(fid,'G01 X%f Y%f Z%f \r\n', p);		   
       end          
    end
end


    
