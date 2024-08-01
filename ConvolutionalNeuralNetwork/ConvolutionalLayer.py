import numpy as np

class ConvLayer:
  def __init__(self, num_filters, filter_size, stride = 1, padding='valid'):
    self.num_filters = num_filters
    self.filter_size = filter_size
    self.stride = stride
    self.padding = padding
    # Init filters with random values
    self.filters = np.random.randn(num_filters, filter_size, filter_size) / (filter_size ** 2)

  # Pads image
  def _pad_input(self, image):
    if self.padding == 'same':
      pad_height = (self.stride * (input.shape[0] - 1) + self.filter_size - input.shape[0]) // 2
      pad_width = (self.stride * (input.shape[1] - 1) + self.filter_size - input.shape[0]) // 2
      padded_input = np.pad(input, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')
    elif self.padding == 'valid':
      padded_input = image
    return padded_input

  # Does convolution
  def _convolve(self, input, filter):
    input_height, input_width = input.shape
    filter_height, filter_width = filter.shape

    output_height = (input_height - filter_height) // self.stride + 1
    output_width = (input_width - filter_width) // self.stride + 1
    output = np.zeros((output_height, output_width))

    for i in range(output_height):
      for j in range(output_width):
        h_start = i * self.stride
        h_end = h_start + filter_height
        w_start = j * self.stride
        w_end = w_start + filter_width
        output[i, j] = np.sum(input[h_start:h_end, w_start:w_end] * filter)

    return output
  
  def forwardPass(self, input):
    self.input = self._pad_input(input)
    self.output = np.zeros((self.num_filters, 
                        (self.input.shape[0] - self.filter_size) // self.stride + 1, # Height of output feature map
                        (self.input.shape[1] - self.filter_size) // self.stride + 1)) # WIdth of output feature map
    for f in range(self.num_filters):
      self.output[f] = self._convolve(input, self.filters[f])

    return self.output

  def backprop(self, d_output, learning_rate):
    # Update filters
    d_filters = np.zeros_like(self.filters, dtype=np.float64)
    input_padded = self._pad_input(self.input)

    for f in range(self.num_filters):
      for i in range(d_filters.shape[1]):
        for j in range(d_filters.shape[2]):
          region = input_padded[i:i+d_output.shape[1]*self.stride:self.stride, 
                                  j:j+d_output.shape[2]*self.stride:self.stride]
          d_filters[f, i, j] = np.sum(region * d_output[f])
    self.filters -= learning_rate * d_filters

    # Calculate Gradient
    d_input = np.zeros_like(self.input, dtype=np.float64)

    for f in range(self.num_filters):
      for i in range(d_output.shape[1]):
        for j in range(d_output.shape[2]):
          h_start = i * self.stride
          h_end = h_start + self.filter_size
          w_start = j * self.stride
          w_end = w_start + self.filter_size
          d_input[h_start:h_end, w_start:w_end] += self.filters[f] * d_output[f,i,j]

    # Remove and padding
    if self.padding == 'same':
      pad_height = (self.input.shape[0] - self.filters.shape[1]) // 2
      pad_width = (self.input.shape[1] - self.filters.shape[2]) // 2
      d_input = d_input[pad_height:-pad_height, pad_width:-pad_width]
    
    return d_input

# input = np.array([
#     [1, 2, 3, 0],
#     [4, 5, 6, 1],
#     [7, 8, 9, 2],
#     [3, 2, 1, 0]
# ])

# filter = np.array([
#     [1, 0],
#     [0, -1]
# ])

# d_output = np.array([
#     [
#         [0.1, 0.2, 0.3],
#         [0.4, 0.5, 0.6],
#         [0.7, 0.8, 0.9]
#     ],
#     [
#         [0.9, 0.8, 0.7],
#         [0.6, 0.5, 0.4],
#         [0.3, 0.2, 0.1]
#     ]
# ])


# testLayer = ConvLayer(num_filters=2, filter_size=2)

# convolvedMatrix = testLayer._convolve(input, filter)
# forwardOutput = testLayer.forwardPass(input)
# backpropOutput = testLayer.backprop(d_output=d_output, learning_rate=1)
# newForward = testLayer.forwardPass(input)

# print("Convolved Matrix:")
# print(convolvedMatrix)
# print("Forward Output:")
# print(forwardOutput)
# print("Backpropogation:")
# print(backpropOutput)
# print("New Forward Pass")
# print(newForward)
