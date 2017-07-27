import tensorflow as tf
import preprocessing as prep
import numpy as np
import scipy.io as sio

def main():

    training_rates = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    learning_rate, iters = 0.25, 1000
    path_pixel, path_sdr = 'nn_results_icub/softmax_icub_pixel/', 'nn_results_icub/softmax_icub_sdr/'

    for ii in range(len(training_rates)):
       
        dataset, train_rate = 'sdrIO/', int(training_rates[ii]*100) # change this line for COIL100 and pi
        dset = dataset + str(train_rate)

        train_x_path, train_header = dset + '/training_x.mat', 'training_x'
        train_hot_y_path, train_hot_y_header = dset + '/hot_training_y.mat', 'hot_training_y'

        test_x_path, test_header = dset + '/testing_x.mat', 'testing_x'
        test_hot_y_path, test_hot_y_header = dset + '/hot_testing_y.mat', 'hot_testing_y'

        train_data_X = prep.extract_mat_content(train_x_path, train_header)
        train_data_Y = prep.extract_mat_content(train_hot_y_path, train_hot_y_header)

        test_data_X = prep.extract_mat_content(test_x_path, test_header)
        test_data_Y = prep.extract_mat_content(test_hot_y_path, test_hot_y_header)

        rows_tr_x, cols_tr_x = train_data_X.shape[0], train_data_X.shape[1]
        rows_tr_y, cols_tr_y = train_data_Y.shape[0], train_data_Y.shape[1]

        #  "Create the model variables"
        X = tf.placeholder(tf.float32, [None, cols_tr_x])
        W = tf.Variable(tf.zeros([cols_tr_x, cols_tr_y]))
        b = tf.Variable(tf.zeros([cols_tr_y]))

        Y_pred = tf.nn.softmax(tf.matmul(X, W) + b)
        Y_actual = tf.placeholder(tf.float32, [None, cols_tr_y])

        # cross_entropy as loss/cost function
        cross_entropy = tf.reduce_mean(-1 * tf.reduce_sum(Y_actual * tf.log(Y_pred), reduction_indices=[1]))
        train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)

        # establish a session
        sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()

        for _ in xrange(iters):
            sess.run(train_step, feed_dict={X: train_data_X, Y_actual: train_data_Y})

        correct_prediction = tf.equal(tf.argmax(Y_pred, 1), tf.argmax(Y_actual, 1))

        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print " training rate: ", train_rate, " accuracy ", sess.run(accuracy, feed_dict={X: test_data_X, Y_actual: test_data_Y}) * 100

        prediction, actual = tf.argmax(Y_pred, 1), np.argmax(test_data_Y, 1)
        pred_mat = prediction.eval(feed_dict={X: test_data_X}, session=sess)
              
        sio.savemat(path_sdr + 'prediction_sdr_smax_' + str(int(training_rates[ii] * 100)) + '.mat',mdict={'prediction_smax_1000': pred_mat})
        sio.savemat(path_sdr + 'actual_y_sdr_smax_' + str(int(training_rates[ii] * 100)) + '.mat', mdict={'actual_y_smax': actual})

if __name__ == '__main__':
    main()