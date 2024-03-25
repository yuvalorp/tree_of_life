this is a web crawler that construct family tree of europe's nobles 

there are two versions of the main:
1. oldest_ancestor - program that use depth search algorithm to find the oldest ancestor of a given person
2. general_main (temporary name) - program that trying to connect as much people as possible to the family tree throw blood connection

the output graph can be presented in two options:
1. pyvis drawer - fully python based graph viewer, it is easy to use and doesn't need internet connection but start lagging in 50 nodes
2. cosmograph drawer - web based graph viewer, it includes more options for displaying data and support very big graphs, but it doesn't open automatically and requires internet connection

the program also includes two layers of cache to minimize http spamming:

first layer cached the wikipadia page which is the raw response and also a processed version that is mach smaller and contain only nessery information  