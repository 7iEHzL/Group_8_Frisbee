clear all; close all; clc

X1=load("data.txt");
X2=load("data.csv");

A=X1;
figure(1);
plot(A(:,1),A(:,2),'g.')
hold on;
plot(A(:,1),A(:,2),"ro")
hold off;

