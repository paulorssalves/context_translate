# context_translate
	
Um script para, de uma lista .csv, pegar palavras e frases em contexto e suas respectivas traduções e enviar para outra lista .csv. 

Input:

| palavras iniciais |
|---|
| предложение |
| достаточно|
| трудно|
| добрый |

Output:

| palavras iniciais | tradução | frase | tradução da frase |
|---|----|----|----|
| предложение | suggestion | três exemplos em russo | três exemplos em inglês |*
| достаточно| enough\*\* |três exemplos em russo | três exemplos em inglês |
| трудно| difficult |três exemplos em russo | três exemplos em inglês |
| добрый | good |três exemplos em russo | três exemplos em inglês |

- *Importante: russo e inglês são simplesmente o que está configurado. Qualquer outra língua selecionável no reverso context funciona, só tem que editar o código fonte.

- \*\* cinco exemplos, se disponíveis 




