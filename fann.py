from fann2 import libfann
import csv

connection_rate = 1
learning_rate = 0.7
num_neurons_hidden = 100

desired_error = 0.0001
max_iterations = 100
iterations_between_reports = 1

early_stopping_threshold = 3
break_on_early_stopping = False

ann = libfann.neural_net()


train_data = libfann.training_data()
train_data.read_train_from_file("data/dev-kmeans-10-pca.data")
# train_data.scale_input_train_data(0, 1)

# ann.create_from_file("minimal.net")
ann.create_sparse_array(connection_rate, (train_data.num_input_train_data(), 40, 20, 10, train_data.num_output_train_data()))

ann.set_learning_rate(learning_rate)
ann.set_activation_function_output(libfann.SIGMOID)


test_data = libfann.training_data()
test_data.read_train_from_file("data/test-kmeans-10-pca.data")
# test_data.scale_input_train_data(0, 1)

count = 0
prev_train_error = 0
prev_test_error = 0
stopped_early = False
early_stopping_point = None
# this is like the following command with early stopping
# ann.train_on_data(train_data, max_iterations, iterations_between_reports, desired_error)
with open('data/fann.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Iteration', 'Train Error', 'Test Error'])
    for i in range(max_iterations):
        ann.train_epoch(train_data)
        train_error = ann.test_data(train_data)
        test_error = ann.test_data(test_data)
        writer.writerow([i+1, train_error, test_error])

        if train_error <= desired_error:
            print "Training Complete: Error Less than %f" % desired_error
            break

        if train_error <= prev_train_error and test_error >= prev_test_error and not stopped_early:
            count = count + 1
            if count >= early_stopping_threshold:
                print "Stopping Early"
                stopped_early = True
                early_stopping_point = train_error
                if break_on_early_stopping:
                    break
        else:
            count = 0

        print "%s Train error: %f, Test error: %f" % (i+1, train_error, test_error)
        prev_train_error = train_error
        prev_test_error = test_error


ann.save("minimal.net")
print "\nTrain error: %f, Test error: %f\n\n" %(ann.test_data(train_data),ann.test_data(test_data))

if early_stopping_point is not None:
    print "Early stopping point %f" % early_stopping_point