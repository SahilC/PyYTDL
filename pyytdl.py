import sys
import re
import urllib
import urlparse
import os
fmts = {
        13:('.3gp', '3gp Low 144p'),
        17:('.3gp', '3gp Med 144p'),
        36:('.3gp', '3gp Hi 240p'),
        5:('.flv', 'Flv Low 240p'),
        34:('.flv', 'Flv Med 360p'),
        6:('.flv', 'Flv Med2 360p'),
        35:('.flv', 'Flv Hi 480p'),
        43:('.webm', 'webm 480p'),
        44:('.webm', 'webm HD 720p'),
        45:('.webm', 'webm HD2 720p'),
        46:('.webm', 'webm HD3 1080p'),
        18:('.mp4', 'mp4 Hi 360p'),
        22:('.mp4', 'mp4 HD 720p'),
        37:('.mp4', 'mp4 HD2 1080p'),
        38:('.mp4', 'mp4 HD3 3072p')
        }

fmt_priority = [38, 37, 22, 18, 46, 45, 44, 43, 35, 6, 34, 5, 36, 17, 13]

def download_progress(count, block_size, total_size):
    percent = int( (count*block_size*100)/total_size )
    sys.stdout.write("\r[" + '#' * (percent/2) + '-' * (50 - percent/2)  + "] %3d%% of %d MB" % (percent, total_size/(1024 * 1024)) )

if __name__=='__main__':
	print 'Input the Youtube URL for Video'
	url=raw_input()
	vidid=re.search(r'(?i)watch\?.*v=([^\&]*).*', url).group(1)
	video_info = urlparse.parse_qs(urllib.urlopen(r'http://www.youtube.com/get_video_info?video_id='+ vidid+ "&asv=3&el=detailpage&hl=en_US").read())
	if video_info['status'][0].lower()!='ok':
		print 'Cannot download this file'
		sys.exit(1)
	video_title = video_info['title'][0]
	print 'Title: ' + video_title
	vid_list={}
	for vid in video_info['url_encoded_fmt_stream_map'][0].split(','):
		v=urlparse.parse_qs(vid)
		vid_list[int(v['itag'][0])]=v['url'][0]+'&signature='+v['sig'][0]
	choice = 0
	quality=0
	while 1:
		print '[?] Choose format:'
       		for fmt in fmt_priority:
        	        if fmt in vid_list.keys():
        	            print '\t[%2d] %s' % (fmt, fmts[fmt][1])
	
        	try:
        	        choice = int(raw_input('\tChoice? '))
        	        if choice in vid_list.keys():
        	            break
        	except:
        	        pass

	name = re.sub(r'[^A-Za-z0-9-_.]+', ' ', video_title)
	name+=fmts[choice][0]
	if os.path.exists(name):
        	print '[!] \"%s\" already exists on disk, skipping!' % (name, )
	else:	
        	urllib.urlretrieve(vid_list[choice], name, reporthook=download_progress)


