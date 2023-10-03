%% ACELEROMETROS SINCRONIZACIÓN
%% Lectura de archivos

close all
clear all

Date = '1204';

% Frecuencias medidas
Freq = [0.5, 1, 2, 3.1, 5, 10, 20, 31.5, 50];
FreqStr = {'0p5','1','2','3p1','5','10','20','31p5','50'};
Folder  = 'C:\Users\Constanza\OneDrive - fi.uba.ar\TESIS\Acelerometros\1204ensayo\Analogicos';
%% Datos muestreo
fs   = 500;
DT   = 1/fs;
Tend = 60;
Tini = 10
%% Lectura de archivos

% Lectura del .dat para los 2 uniaxiales y el RION y 9 ensayos [Array (Ensayo)]
for j=1:9 %Ensayo 1 a 9
 Filename = strcat(Date,'_',FreqStr{j},'_'); % Filename
 datos {j} = f_LeerRIONUNI(Folder, Filename,Tend,Tini,fs); %t RION uni1 uni2
end

%% Correlación cruzada UNI
for j=1:9
[r12(:,j),lags(:,j)] = xcorr(datos{j}(:,3),datos{j}(:,4),'normalized');
t2 = lags*DT;
[pk12,ind] = max (r12(:,j)); %Maximo
tpk12 (:,j)= t2(ind);         %Lag pico
end

%Grafico Lag
figure;
plot(Freq,abs(tpk12),'s-','linewidth',1);
ylim([0 0.01]);
legend({'1 vs 2'},'Location','northwest')
set(gca,'XTick',[0.5 1 2 3.1 5 10 20 31.5 50]);
set(gca,'xscale','log');
xlabel('Frecuencia (Hz)');
ylabel('Lag (s)');
title('Sincronización Uniaxiales');
grid on


%Grafico Lag/Periodo
figure;
plot(Freq,abs(tpk12).*Freq,'s-','linewidth',1);
legend({'1 vs 2'},'Location','northwest')
set(gca,'XTick',[0.5 1 2 3.1 5 10 20 31.5 50]);
set(gca,'xscale','log');
ylim([0 0.1]);
xlabel('Frecuencia (Hz)');
ylabel('Lag/Periodo');
title('Sincronización Uniaxiales');
grid on


%Grafico Lag/DT (muestreo)
figure;
plot(Freq,abs(tpk12)/DT,'s-','linewidth',1);
legend({'1 vs 2'},'Location','northwest')
set(gca,'XTick',[0.5 1 2 3.1 5 10 20 31.5 50]);
set(gca,'xscale','log');
ylim([0 6]);
xlabel('Frecuencia (Hz)');
ylabel('Lag/DT');
title('Sincronización Uniaxiales');
grid on


