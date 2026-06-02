$ =====================================================================
$ ASIGNACIÓN II - LENGUAJE L (PROGRAMA 1)
$ Algoritmo: Desconexión de cargas críticas ante caída de potencia
$ =====================================================================

RED principal = 600;        $ Capacidad actual simulada en estado de falla (< 200 kW)
CARGA hospital = 300;       $ Carga crítica (Prioridad Máxima)
CARGA industrias = 150;     $ Carga secundaria (Prioridad Media)
CARGA residencial = 100;    $ Carga residencial (Prioridad Baja)

SI (principal < 200) {
    DESCONECTAR(residencial);
    principal = principal + 100; 
    
    SI (principal < 200) {
        DESCONECTAR(industrias);
    }
} SINO {
    CONECTAR(residencial);
    CONECTAR(industrias);
}