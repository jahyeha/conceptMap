# 첫 번째 검색 우선 매핑 결과



매핑결과들1 : `5u0jaA3qAGk`에서 임의로 뽑은 컨셉들 18개 대상으로 URL 매핑 

18개중 4개 틀리게 매핑



매핑결과들2 : BOW의 `[5, 11, 20, 22, 30]`번째 결과들로 URL 매핑

['force', 'gravity', 'mass', 'acceleration', 'lift']에서 lift 틀리게 매핑

['velocity', 'motion', 'wheel', 'acceleration', 'times']에서 motion, times 틀리게 매핑

['gas', 'temperature', 'volume', 'expansion', 'pressure']에서 expansion 틀리게 매핑

['heat', 'temperature', 'energy', 'water', 'system']에서 틀리게 매핑된것 없음

['resistor', 'voltage', 'circuit', 'drop', 'resistance']에서 circuit, drop, resistance 틀림



## 매핑결과들1

```
['neural network', 'python', 'predictions', 'Cost function', 'weights', 'synapses', 'Machine learning', 'curse of dimensionality', 'neural Network', 'precision', 'evaluations ', 'optimization', 'computational time', 'gradient descent', 'dimension', 'non convex', 'squared errors', 'non convex Loss functions']
```

위 18개의 단어셋에서 매핑한 결과 18개 중 틀린 링크 목록(모호하게 찾은 결과)은 아래와 같음

python to ('Python', '<https://en.wikipedia.org/wiki/Python>') : 모호하게 찾음

Cost function to ('Cost function', '[https://en.wikipedia.org/wiki/Cost function](https://en.wikipedia.org/wiki/Cost> function)') : Loss function을 찾아야함(모호하게 찾음)

weights to ('Weight (disambiguation)', '<https://en.wikipedia.org/wiki/Weight> (disambiguation)') : 모호하게 찾음

precision to ('Precision', '<https://en.wikipedia.org/wiki/Precision>') : 모호하게 찾음



18개의 결과중 위 4개가 모호한(틀린) 결과로 매핑함



### 결과 데이터

['neural network', 'python', 'predictions', 'Cost function', 'weights', 'synapses', 'Machine learning', 'curse of dimensionality', 'neural Network', 'precision', 'evaluations ', 'optimization', 'computational time', 'gradient descent', 'dimension', 'non convex', 'squared errors', 'non convex Loss functions']

neural network to ('Artificial neural network', 'https://en.wikipedia.org/wiki/Artificial neural network')

python to ('Python', 'https://en.wikipedia.org/wiki/Python')

predictions to ('Prediction', 'https://en.wikipedia.org/wiki/Prediction')

Cost function to ('Cost function', 'https://en.wikipedia.org/wiki/Cost function')

weights to ('Weight (disambiguation)', 'https://en.wikipedia.org/wiki/Weight (disambiguation)')

synapses to ('Synapse', 'https://en.wikipedia.org/wiki/Synapse')

Machine learning to ('Machine learning', 'https://en.wikipedia.org/wiki/Machine learning')

curse of dimensionality to ('Curse of dimensionality', 'https://en.wikipedia.org/wiki/Curse of dimensionality')

neural Network to ('Artificial neural network', 'https://en.wikipedia.org/wiki/Artificial neural network')

precision to ('Precision', 'https://en.wikipedia.org/wiki/Precision')

evaluations  to ('Evaluation', 'https://en.wikipedia.org/wiki/Evaluation')

optimization to ('Mathematical optimization', 'https://en.wikipedia.org/wiki/Mathematical optimization')

computational time to ('Time complexity', 'https://en.wikipedia.org/wiki/Time complexity')

gradient descent to ('Gradient descent', 'https://en.wikipedia.org/wiki/Gradient descent')

dimension to ('Dimension', 'https://en.wikipedia.org/wiki/Dimension')

non convex to ('Convex set', 'https://en.wikipedia.org/wiki/Convex set')

squared errors to ('Mean squared error', 'https://en.wikipedia.org/wiki/Mean squared error')

non convex Loss functions to ('Loss functions for classification', 'https://en.wikipedia.org/wiki/Loss functions for classification')





## 매핑 결과들2



['force', 'gravity', 'mass', 'acceleration', 'lift']에서 lift 틀리게 매핑

['velocity', 'motion', 'wheel', 'acceleration', 'times']에서 motion, times 틀리게 매핑

['gas', 'temperature', 'volume', 'expansion', 'pressure']에서 expansion 틀리게 매핑

['heat', 'temperature', 'energy', 'water', 'system']에서 틀리게 매핑된것 없음

['resistor', 'voltage', 'circuit', 'drop', 'resistance']에서 circuit, drop, resistance 틀림

#### 5 ['force', 'gravity', 'mass', 'acceleration', 'lift']

##### 틀린 데이터 5개 중 1개

```
lift 
```

##### 전체데이터

5 ['force', 'gravity', 'mass', 'acceleration', 'lift']

force to ('Force', 'https://en.wikipedia.org/wiki/Force')

gravity to ('Gravity', 'https://en.wikipedia.org/wiki/Gravity')

mass to ('Mass', 'https://en.wikipedia.org/wiki/Mass')

acceleration to ('Acceleration', 'https://en.wikipedia.org/wiki/Acceleration')

lift to ('Lift', 'https://en.wikipedia.org/wiki/Lift')



#### 11 ['velocity', 'motion', 'wheel', 'acceleration', 'times']

틀린 결과 5개중 2개

```
motion, times
```

##### 전체데이터

velocity to ('Velocity', 'https://en.wikipedia.org/wiki/Velocity')

motion to ('Motion', 'https://en.wikipedia.org/wiki/Motion')

wheel to ('Wheel', 'https://en.wikipedia.org/wiki/Wheel')

acceleration to ('Acceleration', 'https://en.wikipedia.org/wiki/Acceleration')

times to ('The Times (disambiguation)', 'https://en.wikipedia.org/wiki/The Times (disambiguation)')



#### 20 ['gas', 'temperature', 'volume', 'expansion', 'pressure']

틀린 결과

```
expansion 
```

##### 전체 데이터

gas to ('Gas', 'https://en.wikipedia.org/wiki/Gas')

temperature to ('Temperature', 'https://en.wikipedia.org/wiki/Temperature')

volume to ('Volume', 'https://en.wikipedia.org/wiki/Volume')

expansion to ('Expansion', 'https://en.wikipedia.org/wiki/Expansion')

pressure to ('Pressure', 'https://en.wikipedia.org/wiki/Pressure')



#### 22 ['heat', 'temperature', 'energy', 'water', 'system']

틀린 데이터

```
없음?
```

##### 전체 데이터

22 ['heat', 'temperature', 'energy', 'water', 'system']

heat to ('Heat', 'https://en.wikipedia.org/wiki/Heat')

temperature to ('Temperature', 'https://en.wikipedia.org/wiki/Temperature')

energy to ('Energy', 'https://en.wikipedia.org/wiki/Energy')

water to ('Water', 'https://en.wikipedia.org/wiki/Water')

system to ('System', 'https://en.wikipedia.org/wiki/System')



#### 30 ['resistor', 'voltage', 'circuit', 'drop', 'resistance']

틀린 데이터

```
circuit, drop, resistance
```

##### 전체 데이터

resistor to ('Resistor', 'https://en.wikipedia.org/wiki/Resistor')

voltage to ('Voltage', 'https://en.wikipedia.org/wiki/Voltage')

circuit to ('Circuit', 'https://en.wikipedia.org/wiki/Circuit')

drop to ('Drop', 'https://en.wikipedia.org/wiki/Drop')

resistance to ('Resistance', 'https://en.wikipedia.org/wiki/Resistance')

