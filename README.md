# Genetic TSP Algorithm

**The Problem**  
The travelling salesman problem (TSP) asks the following question:  
Given a list of cities[CAPITALS] and the distances[COORDINATES] between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?  

It is an NP-hard problem in combinatorial optimization, important in theoretical computer science and operations research.  

**Chosen Solution**  
Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on biologically inspired operators such as mutation, crossover and selection.

**The Process**  
- Using a list of all nation's capitals and their coordinates(lat,lon)  
- Starting from a "population" of size (N) of randomly generated routes passing through each city (Genome)  
- Fitness Scores are assoicaited to each route based on the total length(km) of the route. (Calculated using city coordinates and circumferance of the earth)  
- "Parents" of the next "generation" of the current population are randomly selected (higher selection chance for higher scores)  
- A "Child" solution is created by splicing the two parents "Genomes"  
- This will repeat until an enirely new "Population" of size (N) consisting of "Children" has been created
- A total of 2000 generations will be examined

**Initial Results** 

Random Weighted Pool Selection using various population sizes
https://github.com/dillondornellas/GeneticAlgorithmTSP/blob/8cf468bec26021d12db040d9e3159099c6b36c37/video/pop10_detail.gif
![image](https://user-images.githubusercontent.com/59612532/128558027-7501d013-563d-4a76-933c-ccd1c96e187c.png)

Visualization of the best result (Population Size 10 | Fitness Score : 900,000km) 
- It can be seen that increasing population size yields worse results.
- Although it might seem that having a larger population with more routes would yield better results, it seems that having a larger population results in better solutions not being selected as often to be "parents" 

![alt text](https://github.com/dillondornellas/GeneticAlgorithmTSP/blob/8cf468bec26021d12db040d9e3159099c6b36c37/video/pop10_detail.gif?raw=true)

Improved Competitive Pool Selection using various population sizes

![image](https://user-images.githubusercontent.com/59612532/128561729-ab77676a-101f-4189-ae16-c1498087d411.png)

Visualization of the best result (Population Size 50 | Fitness Score : 500,000km) 
- Modifying the "Parent" selection by selecting a random group from the population and having them fight (based on inverse fitness score) makes it more likely that stronger parents are selected.
- This should allow for larger populations to be used since stronger parents are more likely to pass on its "Genes" 
- **This has resulted in an improvement of 43.66% over that past method**  
- 
![alt text](https://github.com/dillondornellas/GeneticAlgorithmTSP/blob/8cf468bec26021d12db040d9e3159099c6b36c37/video/pop50.gif?raw=true)


