# SWATCUPPython

Interface python para uso do SWATCUP. Oferece funcões simles para controle e 
automação do otimizador SWATCUP.

Em desenvolvimento. Não é recomendado o uso nesse momento.

## Problemas conhecidos
- No Linux é preciso ter cuidado com a caixa alta e caixa baixa do texto. Em windows 
isso não faz diferença, mas no Linux são arquivos diferentes, e pode dar problema
na execução. 
- O caracter de fim de linha utilizado no Linux é diferente do Windows.
Pode ser necessário utilizar o comando```dos2unix *``` nos arqvuio no Linux para converter
os arquivos, caso esteja tendo problema de fim de arquivo ou de linha.
- Ainda não é possível utilizar esse sistema no Windows
- Ao importar projetos do Windows pode ocorrer um problema esqusito de aparecer mais de 
uma arquivo com mesmo nome mas com caixa diferente. Para evitar isso faça um zip
do projeto no Windows, e descompacte no Linux. 
- Os nomes de arquivos e caixa do texto não são consistentes dentro do SWATCUP, esteja
preparado para problemas estranhos com relação ao nome dos arquivos do projeto. Esse
problema se deve ao fato de no Windows a caixa de texto não é importante ao lidar com
nome dos arquivos, e no Linux sim. Como o desenvolvimento do SWATCUP foi inicialmente
em Windows, os desenvolvedores não devem ter notado que não estava utilizando os 
nomes de arquivos de forma consistente.
- O resultado é diferente rodando em linux ou em windows. O SUFI2_Pre gera parametros
iguais para cada variavel, mas combina ele de forma diferente. Para um mesmo conjunto
de parametros os valores de saída são próximos, mas não iguais. A implementação deve ser 
ligeiramente diferente.

## TODO
- Processamento paralelo
- Funcionar no Windows
- Fazer um check entre o numero de rodadas do par_inf e swEDIT, eles precisam 
ser iguais e é uma boa fonte de erro



## Processamento paralelo
No processamento paralelo rodado primeiro o SUFI2_pre no diretório raiz. Em seguida 
um processo é rodado para salvar os dados no diretorios parallelporcessing/#processo, colocar acho
que alguns arquivos na RAM (diretório Backup and arquivos do projeto) e o SUFI2_run.bat
é executado em cada diretorio. Aparentemente o SWAT-Edit.exe tem uma rotina interna
que detecta o diretorio que ele está e altera o funcionamento para modo paralelo.
Ainda não descobri como ele faz para acessar os dados do Backup e do Projeto, acredito
que fica na RAM e é acessado de alguma forma. Passei um decompilador C# o SWAT-Edit.exx
mas ainda não esta claro como ele faz isso). No final é executado o SUFI2_Stop.bat no 
diretório raiz do projeto para coletar os dados.