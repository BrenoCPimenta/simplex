# Simplex
Pesquisa Operacional, 2021/1

#### Execução:
```sh
python3 main.py < nome.arquivo
```


#### Input:
A primeira linha da entrada contem dois inteiros n e m, o número de restrições e variáveis respectivamente.
A segunda linha contém m inteiros, ci , que formam o vetor de custo.
Cada uma das n linhas seguintes contém m + 1 inteiros que representam as restrições. Para a i-ésima linha, os m primeiros números são a(i,1), a(i,2), ... , a(i,m) enquanto o último é bi.

#### Output:
* Caso a PL possua um **valor ótimo**, será impresso o 'otima' na primeira linha e o valor na segunda. Na terceira linha, será escrito a solução e na útlima o certificado de otimalidade.
* Para o caso em que a PL é **inviável**, a primeira linha terá escrito 'inviavel' e na segunda linha terá o certificado de inviabilidade.
* Para o caso em que a PL é **ilimitada**, escreva, na primeira linha, ilimitada. Na segunda linha, escreva uma solução viável. E, na terceira linha, escreva um certificado de ilimitabilidade.

#### Arquivos:
* **main:** possui a leitura de aquivos e o fluxo de execução.
* **PL:** contém o simplex e os métodos de execução da primal.
* **Auxiliar:** recebe uma PL em FPI e gera uma PL auxiliar.

#### Detalhes da execução:
Coloca a entrada em FPI, verifica a necessidade do uso de uma PL auxiliar para verificar viabilidade.
Ao utilizar PL auxiliar, há o reaproveitamento dos pivoteamentos realizados.
Após a verificação de viabilidade o simplex é resolvido através de pivoteamento.
> É possível alterar uma flag de print interna ao código e chamar métodos das classes para poder imprimir os passos. No formato atual só é impresso os resultados.
