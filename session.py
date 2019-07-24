import logging
import yaml



logger = logging.getLogger('session.py')


def save(fp, datapath, savepath, csvfilename, min_dur, f_ind, m_ind):
	d = {
		'audio data path': datapath,
		'save path': savepath,
		'csv filename': csvfilename,
		'minimum clip duration': min_dur,
		'file index': f_ind,
		'mini clip index': m_ind
	}
	with open(fp, 'w') as file:
		yaml.dump(d, file)

	logger.info('saved session file to {}'.format(fp))


def load(fp):
	with open(fp, 'r') as file:
		d = yaml.load(file, Loader=yaml.BaseLoader)

	logger.info('loaded session from {}'.format(fp))
	
	return (
		d['audio data path'], 
		d['save path'], 
		d['csv filename'], 
		d['minimum clip duration'], 
		d['file index'], 
		d['mini clip index']
	)
