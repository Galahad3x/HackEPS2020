# HackEPS2020

PuntuacionFactory
```
x1/distancia + x2*lejos + x3*produccion + x4/enemigos + enemiga*x5
```
puntuacionMovimiento(mov, t)
```
sum(fact.nCyborgs) - fDestino.nCyborgs + sum(fact.factProd*max(fact.n,t)) excepte fDestino + fDestino.factGen*(max(fDestino.n calculat amb mov.numeroCyborgs - fDestinonCyborgs,t)-distances(fOrigen,fDestino))
```
Factor de perill: Probabilitat de perdre una factory == Factory punctuation des de la perspectiva de l'enemic  
prob_perdua_segura = probabilitat a la que assumim que perdem la factory  
n de una factory = dies que passaran abans de perdre la factory
```
n de una factory(fact.fp, prob_perdua_segura):
(ln(prob_perdua_segura)/ln(1-fact.fp))
```
