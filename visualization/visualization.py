import numpy as np
import scipy.io as sio
import seaborn as sns
from sklearn.metrics import classification_report


def extract_mat_content(path, header):
    """
    Extract the content of the .mat file.
    :param path: where .mat file exists
    :param header:
    :return: the content of the .mat file
    """
    content = sio.loadmat(path)

    return content[header]


def display_classification_metrics(y_actual, y_prediction):
    """
    Use sklear to display classification metrics; recall, precision, F1 scores
    :param y_actual:     ground-truth of the predicted objects
    :param y_prediction: the predicted objects
    :return: print the   recognition (averaged) values.
    """

    print classification_report(y_actual, y_prediction)

def extract_confusion_matrices(sm_pix_conf_mat, sm_sdr_conf_mat, slp_pix_conf_mat,slp_sdr_conf_mat, mlp_pix_conf_mat, mlp_sdr_conf_mat ):
    """
    Extract the heat maps as confusion matrices and save them as a figure
    :param sm_pix_conf_mat:     confusion matrix of softmax regression with pixel inputs
    :param sm_sdr_conf_mat:     confusion matrix of softmax regression with representation inputs
    :param slp_pix_conf_mat:    confusion matrix of single layer perceptron with pixel inputs
    :param slp_sdr_conf_mat:    confusion matrix of single layer perceptron with representation inputs
    :param mlp_pix_conf_mat:    confusion matrix of multi layer perceptron with pixel inputs
    :param mlp_sdr_conf_mat:     confusion matrix of multi layer perceptron with representation inputs
    :return:
    """

    xticks = np.array(range(50))

    xticks = [str(x) if i % 5 == 0 else '' for i, x in enumerate(xticks)]
    yticks = [str(x) if i % 5 == 0 else '' for i, x in enumerate(xticks)]
    sns.plt.figure(1)
    #print slp_pix_conf_mat
    sns.heatmap(sm_pix_conf_mat, cbar=True, vmin=0, vmax=2,  linewidths=2, yticklabels=yticks, xticklabels=xticks)

    #sns.plt.title("Q Matrix Heatmap", fontweight='bold')
    sns.plt.ylabel("Actual Object IDs", weight='bold')
    sns.plt.xlabel("Recognized Object IDs",weight='bold')
    sns.plt.savefig("Figs/smax_pix.png")

    sns.plt.figure(2)
    sns.heatmap(sm_sdr_conf_mat, cbar=True, vmin=0, vmax=2,  linewidths=2, yticklabels=yticks, xticklabels=xticks)
    sns.plt.ylabel("Actual Object IDs", weight='bold')
    sns.plt.xlabel("Recognized Object IDs", weight='bold')
    sns.plt.savefig("Figs/smax_sdr.png")

    sns.plt.figure(3)
    sns.heatmap(slp_pix_conf_mat, cbar=True, vmin=0, vmax=2, linewidths=2, yticklabels=yticks, xticklabels=xticks)
    sns.plt.ylabel("Actual Object IDs", weight='bold')
    sns.plt.xlabel("Recognized Object IDs", weight='bold')
    sns.plt.savefig("Figs/slp_pix.png")

    sns.plt.figure(4)
    sns.heatmap(slp_sdr_conf_mat, cbar=True, vmin=0, vmax=2, linewidths=2, yticklabels=yticks, xticklabels=xticks)
    sns.plt.ylabel("Actual Object IDs", weight='bold')
    sns.plt.xlabel("Recognized Object IDs", weight='bold')
    sns.plt.savefig("Figs/slp_sdr.png")

    sns.plt.figure(5)
    sns.heatmap(mlp_pix_conf_mat, cbar=True, vmin=0, vmax=2, linewidths=2, yticklabels=yticks, xticklabels=xticks)
    sns.plt.ylabel("Actual Object IDs", weight='bold')
    sns.plt.xlabel("Recognized Object IDs", weight='bold')
    sns.plt.savefig("Figs/mlp_pix.png")

    sns.plt.figure(6)
    sns.heatmap(mlp_sdr_conf_mat, cbar=True, vmin=0, vmax=2, linewidths=2, yticklabels=yticks, xticklabels=xticks)
    sns.plt.ylabel("Actual Object IDs", weight='bold')
    sns.plt.xlabel("Recognized Object IDs", weight='bold')

    sns.plt.savefig("Figs/mlp_sdr.png")
    #manager = sns.plt.get_current_fig_manager()
    #manager.resize(*manager.window.maxsize())
    #manager = sns.plt.get_current_fig_manager()
    #manager.resize(*manager.window.maxsize())
    #sns.plt.savefig("results_full_size.png", figsize=(1640, 860))
    sns.plt.show(block=True)
