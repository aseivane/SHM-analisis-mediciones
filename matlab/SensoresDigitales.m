%% Visualizacion de resultados Sensores Digitales
clear
close all

%% Input
NameIni = '20230719'; %AAAAMMDD
NumMed  = 1;      % 1: Primer Medición 15 min. 2: Ultima Medición 15 min. 

filtrar = 0;
nodos   = 2;   % Cantidad de acelerometros

%% Directorios de cada medición
Ensayo = 'medicion_20230719-015'; %Medicion 15  - 15 minutos. Pulso


% Ruta de cada nodo (relativo a /datos_0xx)
id {1} = 'nodo_34ab958660d0'; 
id {2} = 'nodo_94b97eda9150'; 

% Id medicion
Medicion {1}= '015-';
Medicion {2}= '015-';

%% Lectura de archivos MPU
Channel = 'y';
if strcmp(Channel,'x')
    ch = 2;
elseif strcmp(Channel,'y')
    ch = 3;
elseif strcmp(Channel,'z')
    ch = 4;
end

Extension = '.dat';
Filename = strcat(NameIni,'-',Medicion{NumMed});


for ii = 1:nodos % Acelerometro 1 a 2
    Carpeta  = fullfile(Ensayo,id{ii});
    fstruct   = dir(fullfile(Carpeta,strcat(Filename,'*',Extension)));
    Datos    = f_LeerMPUall(fstruct,Carpeta,Filename);
    if ii == 1
        t = Datos(:,1);    % la primera columna es el vector tiempo
        Datos = -Datos;     % eje y al reves
    end
    Acc(:,ii) = (Datos(:,ch)-mean(Datos(:,ch)))*9.806; %resto la media
end


%% Plot
ciclos = 10;
Accmax = max(max(abs(Acc)));
Equipo = {'1','2'};
Create_Window(0.65,0.5);
for ii = 1:2
    subplot(2,1,ii)
    plot(t,Acc(:,ii),'linewidth',0.5);
    xlim([0 200]);
    xlabel('Tiempo(s)');
    ylabel(strcat('Acc-',Equipo{ii}));
    sgtitle ('Aceleración - MPU')
    grid on
    box on
end

%% Picos
pks1 = findpeaks(Acc(:,1),'MinPeakProminence',15);
pks2 = findpeaks(Acc(:,2),'MinPeakProminence',15);
    
%% Correlaciones
[Xcorr1,lag] = xcorr(Acc(:,1),Acc(:,2),'unbiased');


Create_Window(0.65,0.5);
plot(lag*(t(2)-t(1)),Xcorr1,'linewidth',0.5);
  xlabel('Lag (segundos)');
  ylabel(strcat('Xcorr-1vs2'));
  title ('Correlación cruzada')
  grid on
  box on
  xlim([-1 1]);



