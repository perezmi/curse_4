%из файла полученного от робота вытащим в массив
%и разобьем каждый столбец на переменные
inputDataRob = dlmread('lab1_pereverzev_12e_res.txt');
t = inputDataRob(:,1);
omega_1 = inputDataRob(:,2);
omega_2= inputDataRob(:,3);
omega_3= inputDataRob(:,4);
omega_4= inputDataRob(:,5);
M1= inputDataRob(:,6);
M2= inputDataRob(:,7);
M3= inputDataRob(:,8);
M4= inputDataRob(:,9);
Vx_o= inputDataRob(:,10);
Vy_o= inputDataRob(:,11);
dpsi= inputDataRob(:,12);
x0= inputDataRob(:,13);
y0= inputDataRob(:,14);
psi = inputDataRob(:,15);
%откроем файл с данными по идеальным перемещениям
inputDataIdeal = dlmread('lab1_pereverzev_12e_res.txt');
Xid = inputDataIdeal(:,1);
Yid = inputDataIdeal(:,2);
psi_id = inputDataIdeal(:,3);
%откроем файл с данными по идеальным скоростям
inputDataIdSpeed = dlmread('lab1_pereverzev_12e_res.txt');
Vxid = inputDataIdSpeed(:,1);
Vyid = inputDataIdSpeed(:,2);
Omid = inputDataIdSpeed(:,3);
%Найдем рассогласование по координатам
dX = Xid-x0;
dY = Yid -y0;
delPsi = psi_id - psi;
dVx = Vxid - Vx_o;
dVy = Vyid - Vy_o;
ddPsi = Omid - dpsi;
%зададим В - блочную матрицу столбцов свободных членов
integraDVxdt(1,1) = dVx(1,1);
for i = 2:1:length(dVx)
integraDVxdt(i,1) = dVx(i,1)+integraDVxdt(i-1,1);
end
integraDVxdt = integraDVxdt*0.1;
integraDVydt(1,1) = dVy(1,1);
for i = 2:1:length(dVx)
integraDVydt(i,1) = dVy(i,1)+integraDVydt(i-1,1);
end
integraDVydt = integraDVydt*0.1;
integraDdpsi(1,1) = ddPsi(1,1);
for i = 2:1:length(dVx)
integraDdpsi(i,1) = ddPsi(i,1)+integraDdpsi(i-1,1);
end
integraDdpsi = integraDdpsi*0.1;
%зададим В - блочную матрицу столбцов свободных членов
B = zeros(length(dVx)*3,1);
k = 1;
for i = 1:3:((length(dVx)*3))
    B(i,1) = dX(k,1)- integraDVxdt(k,1);
    B(i+1,1) = dY(k,1)- integraDVydt(k,1);
    B(i+2,1) = delPsi(k,1)- integraDdpsi(k,1);
    k = k + 1;
end
%������� � - ������� ������� �������������
A = zeros(length(dVx)*3,1);
k = 1;
for i = 1:3:((length(dVx)*3))
    A(i,1) = Vxid(k,1);
    A(i+1,1) = Vyid(k,1);
    A(i+2,1) = Omid(k,1);
    k=k+1;
end
%��������� ����� ������������
dtzap = inv(A'*A)*A'*B;
%������ ��������������� ����������
for i = 1:1:length(dVx)
Xvost(i,1) = x0(i,1)+Vxid(i,1)*dtzap+integraDVxdt(i,1);
end
for i = 1:1:length(dVx)
Yvost(i,1) = y0(i,1)+Vyid(i,1)*dtzap+integraDVydt(i,1);
end

hold on;
grid on;
for i = 1:1:length(dVx)
plot(x0,y0,'r');
plot(Xid,Yid,'b');
plot(Xvost,Yvost,'g');
end

title('Движение мекано-платформы youBot');
legend({'Движение платформы снятое датчиками','Идеальное предполагаемое движение плафтормы','Восстановленное движение платформы'},'Location','southwest');
