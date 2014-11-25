from fann2 import libfann

connection_rate = 1
learning_rate = 0.7
num_neurons_hidden = 100

desired_error = 0.0001
max_iterations = 100
iterations_between_reports = 1

ann = libfann.neural_net()


train_data = libfann.training_data()
train_data.read_train_from_file("data/dev-kmeans-10-full.data")
# train_data.scale_input_train_data(0, 1)

# ann.create_from_file("minimal.net")
ann.create_sparse_array(connection_rate, (train_data.num_input_train_data(), 20, 10, train_data.num_output_train_data()))

ann.set_learning_rate(learning_rate)
ann.set_activation_function_output(libfann.SIGMOID)

ann.train_on_data(train_data, max_iterations, iterations_between_reports, desired_error)

ann.save("minimal.net")

test_data = libfann.training_data()
test_data.read_train_from_file("data/test-kmeans-10-full.data")
# test_data.scale_input_train_data(0, 1)

print "\nTrain error: %f, Test error: %f\n\n" %(ann.test_data(train_data),ann.test_data(test_data))