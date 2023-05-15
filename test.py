import matplotlib.pyplot as plt

# Define some sample data
x = [1, 2, 3, 4, 5]
y = [3, 5, 4, 6, 7]

# Create a new figure
fig = plt.figure()

# Add a new plot to the figure
ax = fig.add_subplot(111)

# Plot the data on the plot
ax.plot(x, y)

# Display the plot in the terminal
plt.show()

