clc
clear
close all
array=readmatrix("sinstream.csv");
x=1:size(array);
figure (1)
for i=1:8
subplot(8,1,i)
plot(x,array(:,i));
xlim([0,10000])
end