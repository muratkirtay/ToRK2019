import numpy as np
import scipy.io as sio
import seaborn as sns
import visualization as vis
from mHTM.region import SPRegion


def main():

    data_path, sdr_path = 'humanoids2017/iCubBinary/', 'humanoids2017/iCubSDR/'

    nsamples, nbits, pct_active = 500, 1024, 0.4
    num_of_objs, num_of_imgs, seed = 50, 72, 123456789

    kargs = {
        'ninputs': nbits, 'ncolumns': 1024, 'nactive': int(nbits * 0.2), 'global_inhibition': True,
        'trim': 1e-4, 'disable_boost': True, 'seed': seed, 'nsynapses': 75*4, 'seg_th': 5,
        'syn_th': 0.5, 'pinc': 0.001, 'pdec': 0.001, 'pwindow': 0.5, 'random_permanence': True,
        'nepochs': 10, 'log_dir': os.path.join(base_path, '1-1')
    }

    # Build the SP
    sp = SPRegion(**kargs)

    sdrs = np.zeros((num_of_imgs, nbits), dtype=np.int64)

    for j in range(num_of_objs):
        obj_str, count = 'obj'+str(j+1), 0
        obj_path = data_path + obj_str + '.mat'
        data_content = vis.extract_mat_content(obj_path, obj_str)

        for i in range(len(data_content)):
            sp.fit(data_content[i])
            sp_output = sp.predict(data_content[i, :])  
            if np.count_nonzero(sp_output * 1) < int(nbits * 0.2):
                count +=1
            outp = sp_output * 1                
            sdrs[i, :] = outp

        # save .mat files for recognition
        sdr_mat = sdr_path + 'sdrObj' + str(j+1) + '.mat'
        sio.savemat(sdr_mat, mdict={'sdrObj' + str(j+1): sdrs})
        sdrs = np.zeros((num_of_imgs, nbits), dtype=np.int64)

if __name__ == '__main__':
    main()
