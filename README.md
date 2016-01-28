# Generalized Double GNC (GDGNC)

## Overview

This project contains scripts used for my PhD research on software graph shape and generated software graphs.

## Running

### Extracting software dependencies

Software dependencies extractions can be found in the `graphs/real` folder for my dataset used in my paper (see Research Papers section).

#### Prerequisite

To extract real graph dependencies you need to download [dependency finder](http://sourceforge.net/projects/depfind/). Extract the content of the archive somewhere in your system.

#### Dependency finder XML file

To extract the dependency finder xml file, use:

```
depgraph.py <software> <xmlfile> <pathtodepfindbin>
```

This command will extract the xml file to `<xmlfile>`. The file will contains all dependencies contained in the jars found recursively in `<software>`. Note that `<pathtodepfindbin>` is the absolute path to the `bin` folder of the dependency finder project (ie. if I do extract dependency finder in my home dir: `/home/vince/DependencyFinder-1.2.1-beta4/bin/`).

Note that this command will simply find all jar files and invoke:

```
<pathtodepfindbin>/DependencyExtractor <jarsfiles> -xml -out <xmlfile>
```

#### Dependencies

Once you produced an XML file, you can obtain dependencies using:

```
xmldepgraph.py <xmlfile> <outfile> <mode> <granluarity> <depfinder_root> <signaturefilter ...>
```

Parameters:

- `<xmlfile>` the input xml file;
- `<outfile>` the output dependency file;
- `<mode>` indicated if only endo dependencies should be considered. To do so, use __internal__. The opposite is obtained using __external__. Use __all__ to consider all;
- `<granluarity>` indicates the granularity of extracted items, can be: __package__, __class__ or __feature__;
  - `<depfinder_root>`  specify the absolute path to the dependency finder bin folder;
  - `<signaturefilter ...>` specify string which validate an item (according to its signature). Use '!' for default package.

#### Example: extracting ant graph

Let assume I do installed ant in `/home/vince/Temp/ant/` and dependency finder in `/home/vince/Temp/depfinder`. Those two lines will produce `ant.xml` XML file and `and.csv` graph file for internal connections only and at the class granularity:

```
$ python2 depgraph.py /home/vince/Temp/ant/ ant.xml /home/vince/Temp/depfinder/bin
$ python2 xmldepgraph.py ant.xml ant.csv internal class /home/vince/Temp/depfinder/bin ant !
```

### Digraph generation

Generations can be found in the `graphs/experiment-arxiv-1410.7921` and `graphs/generated-examples` folders for my dataset used in my paper (see Research Papers section).

Execute `python2 graphgen.py` to display the help for graph generation.
To generate a graph to the standard output, use:

```
graphgen.py [graph-type-id] [parameters]
```

Parameters are dependent of the chosen generator. Some generator requires a number of nodes (`nodes=x`), some other a number of edges (`edges=x`). Moreover, almost all generators requires some parameters.

#### Available generators


| Nr | Name | Nodes | Edges | Floats parameters | Constants parameters |
|----|------|-------|-------|-------------------|----------------------|
| 0 |                  GNC |  True | False |  |  
| 1 |               GD-GNC |  True | False |                 p, q |  
| 2 |       Baxter & Frean | False |  True |                gamma |  
| 3 |              Vazquez |  True | False |                    p |  
| 4 |          Dorogovtsev |  True | False |  |                 m, A
| 5 |             Grindrod |  True | False |        alpha, lambda |  
| 6 |         Kumar Linear |  True | False |           copyfactor |                    d
| 7 |          Erdos Renyi |  True | False |                    p |  
| 8 |                R-MAT |  True |  True |           a, b, c, d |  
| 9 |             Bollobas | False |  True |   alpha, beta, gamma |    deltain, deltaout
| 10 |                  Goh |  True |  True |  alpha_in, alpha_out |  

#### Examples

GDGNC (graph type id *1*) requires a number of nodes and two parameters, *p* and *q*, thus we can, by example, generate a graph with 50 nodes, p and q = 0.5 by invoking:

```
python2 graphgen.py 1 nodes=50 p=0.5 q=0.5
```

Other examples:

```
python2 graphgen.py 8 nodes=50 edges=50 a=.2 b=.3 c=.4 d=.9
python2 graphgen.py 9 edges=50 alpha=.2 beta=.3 gamma=.4 deltain=10 deltaout=20
```

### Comparing kolmogorov-smirnov distances of programs

Use `ks_scores.py`:

```
ks_scores.py <realcsvfile> [<generationfolder>]
```

This script takes as input a csv file `<realcsvfile>` which describe the software graph and a folder containing a set of csv files `<generationfolder>` to compare with.
In the case if `<generationfolder>` is omitted, then the distance of `<realcsvfile>` will be computed with all other programs in the same folder than `<realcsvfile>`.

### Computing mann-whitney p-value of generated graphs

Use `mw_scores.py`:

```
mw_scores.py <realcsvfile> <generationfolder> [<<othergenerationfolder>]
```

This script takes as input a csv file `<realcsvfile>` which describe the software graph and two folders (`<generationfolder>` and `<othergenerationfolder>`) each containing a set of csv files of generated graphs with two different algorithms. If `<othergenerationfolder>` is omitted, then the generated graphs will be compared to all other software contained in the same folder than `<realcsvfile>`.

### Comparing software shapes using kolmogorov-smirnov p-value

Use `softwareshape.py`:

```
softwareshape.py <softwarefolder>
```

Calculate the komlogorov-smirnov p-value with each pair of software cumulative in-/out- degree distrbution.
Print to the standard output each pair computation details and a summary.

### Plot the software cumulative in-/out- degree distribution

Use `softwareshape_plot.py`:

```
softwareshape_plot.py <softwarefolder> <graphplotfile>
```

Plot the cumulative degree distribution for all software contained in `<softwarefolder>`. Software graphs are __.csv__ files which describes the graph. Two files ares produced (one for in- and another for out- degree): `<graphplotfile>_in.pdf` and `<graphplotfile>_out.pdf`.

## Research Papers

This project is used in the following papers:

  - __Vincenzo Musco__, Martin Monperrus, Philippe Preux. A Generative Model of Software Dependency Graphs to Better Understand Software Evolution (http://arxiv.org/abs/1410.7921).

In this section, I do present the dataset used in this paper and specify values used to obtains my results. Some informations may be redundant with the paper. For a full scientific presentation, please refer to http://arxiv.org/abs/1410.7921.

### Software graph extraction

This section reports the signature filter parameter used for importing the projects.

| Project | Version | Signature filter |
|---------|---------|------------------|
|ant|1.9.2|`ant`, `!`|
|jfreechart|1.0.16|`jfree`, `!`|
|jftp|1.57|`jftp`, `!`|
|jtds|1.3.1|`jtds`, `!`|
|maven|3.3.1|`maven`, `!`|
|hsqldb|2.3.1|`hsqldb`, `!`|
|log4j|2.0b9|`log4j`, `!`|
|squirrelsql|3.5.0|`squirrel`, `!`|
|argouml|0.34|`argouml`, `!`|
|mvnforum|1.3|`mvnforum`, `!`|
|atunes|3.1.2|`atunes`, `!`|
|jedit|5.2.0|`jedit`, `!`|
|weka|3.7.12|`weka`, `!`|
|jetty|9.2.7|`jetty`, `!`|
|vuze|5.5|`aelitis`, `!`|

### Software generation best parameters

This section report the parameters used to generate graphs for each software.

| Project | #Nodes | #Edges | Erdos | GDGNC | Baxter & Frean |
|---------|--------|--------|-------|-------|----------------|
|ant|1252|5763|p=0.00368|p=0.4, q=1.0|gamma=0.4|
|jfreechart|858|4783|p=0.00650|p=0.5, q=0.7|gamma=0.3|
|jftp|173|736|p=0.02459|p=0.5, q=0.6|gamma=0.3|
|jtds|90|328|p=0.04049|p=0.9, q=0|gamma=0.3|
|maven|1515|6933|p=0.00302|p=0.8, q=0.1|gamma=0.3|
|hsqldb|602|4976|p=0.01373|p=0.7, q=0.5|gamma=0.2|
|log4j|895|4136|p=0.00516|p=0.5, q=0.6|gamma=0.3|
|squirrelsql|2288|10141|p=0.00194|p=0.6, q=0.5|gamma=0.4|
|argouml|2664|13445|p=0.00189|p=0.4, q=1.0|gamma=0.4|
|mvnforum|282|1614|p=0.02030|p=0.7, q=0.4|gamma= 0.2|
|atunes|1881|8502|p=0.00240|p=0.4, q=1.0|gamma=0.4|
|jedit|1277|5674|p=0.00348|p=0.7, q=0.2|gamma=0.4|
|weka|2860|14082|p=0.00172|p=0.4, q=0.9|gamma=0.4|
|jetty|1908|8798|p=0.00242|p=0.4, q=0.9|gamma=0.4|
|vuze|4633|18493|p=0.00086|p=0.6, q=0.5|gamma=0.4|

## Data structures

All graphs are descried in CSV files where each line describe a directed edge separated by `;`.

## Dependencies

Those scripts runs on __Python 2__. Following libraries are requires:

 - networkx
 - numpy
 - matplotlib
 - scipy

## Contact

See: http://www.vmusco.com or http://www.vincenzomusco.com
