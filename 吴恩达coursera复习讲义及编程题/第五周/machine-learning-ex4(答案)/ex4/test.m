function  [J] = test(X,y,Theta1,Theta2)
 
 num_labels =10;
 m = size(X, 1);
 X = [ones(m, 1) X];
 s = 0; 
 for  i = 1:m
     yt = zeros(10,1);
     yt(y(i)) = 1;
     z2 = Theta1*X(i,:)';
     a2 = sigmoid(z2);
     a2 = [1;a2];
     z3 = Theta2*a2;
     a3 = sigmoid(z3);
     temp = -yt.*log(a3) - (ones(10,1)-yt).*log(ones(10,1)-a3);
     s = s + sum(temp);
 end
 
 J = s/m;

 temp1 = Theta1;
 temp1(:,1) = 0;
 temp2 = Theta2;
 temp2(:,1) = 0;
 
 T1 = temp1.^2;
 T2 = temp2.^2;
 s2 = (0.5*(sum(T1(:)) + sum(T2(:))))/m;
 J = J + s2;
 
 s = 0;
TG1=0;TG2=0;
 for  i = 1:m
     yt = zeros(num_labels,1);
     yt(y(i)) = 1;
     z2 = Theta1*X(i,:)';
     a2 = sigmoid(z2);
     a2 = [1;a2];
     z3 = Theta2*a2;
     a3 = sigmoid(z3);
     delta3 = a3 - yt;
     delta2 = (Theta2(:,2:end))'*delta3.*sigmoidGradient(z2);
     TG1 = TG1 + delta2*X(i,:);
     TG2 = TG2 + delta3*a2';
 end
Theta1_grad = TG1/m;
Theta2_grad = TG2/m;

 
end