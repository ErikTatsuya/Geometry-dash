# IDs: 1=Bloco, 2=Espinho, 3=Serra, 4=Portal
# Tipos: s=ship, w=wave, c=cube, gi=grav_inv, gn=grav_norm

LEVEL_01 = (
    # --- Aquecimento: Saltos Simples ---
    "1,0,540;1,40,540;1,80,540;1,120,540;1,160,540;1,200,540;1,240,540;"
    "2,400,500;"               # Espinho único
    "1,600,500;1,640,500;"     # Pequena plataforma
    "2,640,460;"               # Espinho em cima do bloco
    
    # --- Introdução ao Ship: Corredor de Serras ---
    "4,900,300,s;"             # Portal Ship
    "1,1100,100;1,1140,100;1,1180,100;" # Teto
    "3,1300,450;3,1500,150;"   # Serras alternadas (baixo e cima)
    "1,1700,500;1,1740,500;1,1780,500;" # Chão de saída do Ship
    
    # --- Transição de Gravidade (Cube) ---
    "4,1900,300,c;"            # Volta para Cubo
    "4,2000,300,gi;"           # Inverte Gravidade (vai pro teto)
    "1,2200,100;1,2240,100;1,2280,100;1,2320,100;" # Chão no teto
    "2,2280,140;"              # Espinho no teto!
    
    # --- Seção Wave: Zig-Zag ---
    "4,2500,300,w;"            # Portal Wave
    "3,2700,100;3,2700,500;"   # Portão estreito
    "2,2900,300;2,3100,400;2,3300,200;" # Obstáculos para desviar
    
    # --- Reta Final: Decida e Vitória ---
    "4,3500,300,c;4,3550,300,gn;" # Cubo e Gravidade Normal
    "1,3700,540;1,3740,540;1,3780,540;1,3820,540;"
    "2,3900,500;2,3940,500;2,3980,500;" # Salto Triplo Final!
    "1,4200,540;1,4240,540;1,4280,540;"
)