import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
#NavigationToolbar2Tk

x = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
y = np.arange(len(x))
performance = [10,8,6,4,2,1]

plt.bar(y, performance, align='center', alpha=0.5)
plt.xticks(y, x)
plt.ylabel('Usage')
plt.title('Programming language usage')

plt.show()
