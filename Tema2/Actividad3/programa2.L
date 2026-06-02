$ =====================================================================
$ ASIGNACIÓN II - LENGUAJE L (PROGRAMA 2)
$ Algoritmo: Regulación de flujo de batería con fuentes renovables
$ =====================================================================

BATERIA banco_ion_litio = 45;  $ Estado de carga inicial (SoC) en %
GENERADOR panel_solar = 150;   $ Producción fotovoltaica actual en kW
CARGA consumo_total = 120;     $ Demanda de la comunidad en kW

MIENTRAS (banco_ion_litio < 95) {
    SI (panel_solar > consumo_total) {
        CONECTAR(banco_ion_litio);
        banco_ion_litio = banco_ion_litio + 20;
        panel_solar = panel_solar - 30;
    }
    
    SI (panel_solar < consumo_total) {
        SI (banco_ion_litio > 20) {
            banco_ion_litio = banco_ion_litio - 10;
            consumo_total = consumo_total - 5;
        } SINO {
            DESCONECTAR(banco_ion_litio);
            panel_solar = 0;
        }
    }
}