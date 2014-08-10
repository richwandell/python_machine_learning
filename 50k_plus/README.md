50k Plus
=========

This folder is a collection of python based classification algorithms used for determining whether or not an adult makes 50k/yr or less, or over 50k/yr.

The data used has been taken from the UCI Machine Learning Repository. It consists of US Census Bureau data from 2004. The data was pre loaded into an sqlite database using adult_data table for the reference data and adult_test table for the test data. The adult_data table was transformed into numbers to be used in the different algorithms by adding possible values into a list and substituting the list index for the word. In the case of the neural network, in order to keep the input values between 1 and 0, the ratio of index/list size was used.




Citations:

* [UCI Machine Learning Repository Adult Dataset] - Bache, K. & Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
* [Pybrain] - Tom Schaul, Justin Bayer, Daan Wierstra, Sun Yi, Martin Felder, Frank Sehnke, Thomas Rückstieß, Jürgen Schmidhuber. PyBrain. To appear in: Journal of Machine Learning Research, 2010.
* [Scikit-Learn] - Fabian Pedregosa, Gaël Varoquaux, Alexandre Gramfort, Vincent Michel, Bertrand Thirion, Olivier Grisel, Mathieu Blondel, Peter Prettenhofer, Ron Weiss, Vincent Dubourg, Jake Vanderplas, Alexandre Passos, David Cournapeau, Matthieu Brucher, Matthieu Perrot, Édouard Duchesnay. Scikit-learn: Machine Learning in Python, Journal of Machine Learning Research, 12, 2825-2830 (2011) 





[UCI Machine Learning Repository Adult Dataset]:http://archive.ics.uci.edu/ml/datasets/Adult
[Pybrain]:http://www.pybrain.org/
[Scipy]:http://www.scipy.org/
[Scikit-Learn]:http://jmlr.org/papers/v12/pedregosa11a.html