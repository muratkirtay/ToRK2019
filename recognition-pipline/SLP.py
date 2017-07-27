import numpy as np
import preprocessing as prep
import scipy.io as sio
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

def main():

    training_rates = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    num_of_objects = 50  # 100 for COIL-100 

    for i in range(len(training_rates)):

        dataset, train_rate = 'binaryIO/', int(training_rates[i] * 100)  # change this line for COIL100
        dset = dataset + str(train_rate)

        train_x_path, train_header = dset + '/training_x.mat', 'training_x'
        test_x_path, test_header = dset + '/testing_x.mat', 'testing_x'

        train_hot_y_path, train_hot_y_header = dset + '/hot_training_y.mat', 'hot_training_y'
        test_hot_y_path, test_hot_y_header = dset + '/hot_testing_y.mat', 'hot_testing_y'

        train_data_X = prep.extract_mat_content(train_x_path, train_header)
        train_data_Y = prep.extract_mat_content(train_hot_y_path, train_hot_y_header)

        test_data_X = prep.extract_mat_content(test_x_path, test_header)
        test_data_Y = prep.extract_mat_content(test_hot_y_path, test_hot_y_header)


        x_train, y_train = train_data_X, train_data_Y
        x_test, y_test = test_data_X, test_data_Y

        model = Sequential([
            Dense(1024, input_dim=1024), 
            Activation('sigmoid'),
            Dense(num_of_objects),
            Activation('softmax'),
        ])

        dec = 0.
        sgd = SGD(lr=0.01, decay=dec, momentum=0.9, nesterov=False)
        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd,
                      metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=1000, verbose=0)
        score = model.evaluate(x_test, y_test) 
        classes = model.predict(x_test)
        pred, y_t = np.argmax(classes, axis=1) + 1, np.argmax(y_test, axis=1) + 1
         

        print "icub pixel tr_rate: ", training_rates[ii]*100, "accuracy", np.count_nonzero(pred == y_t) / float(pred.shape[0]) * 100

        fname = 'nn_results_icub/slp_icub_pix/'
        sio.savemat(fname + 'prediction_slp_1000_' + str(int(training_rates[ii]*100))+'.mat', mdict={'prediction_slp_1000': pred})
        sio.savemat(fname + 'actual_y_slp_1000_' + str(int(training_rates[ii]*100))+'.mat', mdict={'actual_y_slp_1000': y_t})

if __name__ == '__main__':
    main()