clear all; close all;

A=load("data.txt");

figure(1);
plot(A(:,1),A(:,2),'k.')
title('Randomly Generated Data')

% k-means
opts = statset('Display','final');
[idx,C] = kmeans(A,2,'Distance','cityblock',...
                'Options',opts);

% plot
figure(2);
plot(A(idx==1,1),A(idx==1,2),'r.','MarkerSize',12);
hold on;
plot(A(idx==2,1),A(idx==2,2),'b.','MarkerSize',12);
plot(C(:,1),C(:,2),'kx',...
    'MarkerSize',15,'LineWidth',3);
legend('Cluster 1','Cluster 2','Centroids',...
    'Location','NW');
title 'Cluster Assignments amd Centroids';
hold off;