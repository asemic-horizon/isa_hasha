# is a/has a

This is a simple script that reads through Python codebases and identifies three patterns, converting them to edges in DOT (graphviz) format

### Inheritance, i.e. the "is a" relationship

```py
class Chemistry(Science):
    pass
```

which is represented as

```
Science -> Chemistry
```

### Type hinting in dataclasses ("explicit has-a")

```py

@dataclass
class SeismicData:
    time_series : pd.Series
    severity : float

@dataclass
class Location:
    seismic_data : SeismicData 
```

which is represented as

```
SeismicData -> Location [arrowhead=icurve]
```
### Type hinting in function definition inside classes ("implicit has-a")

```py

class Insurance:
    def add_location(loc : Location)
```

which is represented as

```
Location -> Insurance [arrowhead=icurve]
```

The script produces a valid .DOT file with nodes grouped in subgraphs by file. You can explicitly group nodes inside squares by messing with the function `file_subgraph` so all subgraph names start with the word `cluster`. The script is otherwise easy to customize, but has been useful to me as is.
