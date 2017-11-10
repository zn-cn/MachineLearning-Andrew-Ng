function [Theta,fval,exitflag] = run()
 
 
 input_layer_size = 400;
 hidden_layer_size = 25;
 num_labels =10;
 lambda = 1;
 
Theta1 = randInitializeWeights(400, 25);
Theta2 = randInitializeWeights(25, 10);
initial_theta = [Theta1(:);Theta2(:)];
 options = optimset('GradObj','on','MaxIter',400);
 
 [Theta,fval,exitflag] = fmincg (@(t)(nnCostFunction(t,input_layer_size,hidden_layer_size,num_labels,X,y,lambda)), ...
              initial_theta, options);
          
end