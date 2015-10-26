function Markov()
mu = [1/6 1/3 1/2];
p = [[0, 2/3, 1/3]; [1/3, 1/3, 1/3]; [1/3, 2/3, 0]];
q = [[1, 0]; [1/2, 1/2]; [0, 1]];

acc = 0;
for i = 1:10000
    xstates = xState(2, mu, p);
    ystates = yState(xstates, q);
    if ystates == [2 1 2]
        acc = acc + 1;
    end
end

acc/10000;

xstates = xState(10000, mu, p);
ystates = yState(xstates, q);

acc = 0
for i = 1:length(ystates)
   if ystates(i) == 1
       acc = acc + 1;
   end
end

disp(acc)
end

function states = yState(xstates, q)
    acc = [];
    for i = 1:length(xstates)
        temp = dinverse(q(xstates(i), :));
        acc = [acc temp];
    end
    states = acc;
end
function states = xState(n, mu, p)
    states = [];
    init = dinverse(mu);
    states = [states init];
    for i = 1:n
        init = dinverse(p(init,:));
        states = [states init];
    end
    
end

function state = dinverse(v)
   u = rand;
   acc = 0;
   for i = 1:length(v)
       acc = acc + v(i);
       if u < acc
           break
       end
   end
   state = i;
end