from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from dummy_data import random_scores, random_names

# pip install numpy
# pip install Pillow
# pip3 install pandas

WHITE =	255, 255, 255
BLACK =	  0,   0,   0

WOAJ1_COLOR	= 255, 204,   0
WOAJ2_COLOR	= 128, 128, 128
WOAJ3_COLOR	= 179,  60,   0
WOAJ_COLOR	= [WOAJ1_COLOR, WOAJ2_COLOR, WOAJ3_COLOR]

header_font = "fonts/FreeMono.ttf" 
header_font_size = 15
names_font = "fonts/FreeMono.ttf"
names_font_size = 30
numbers_font = "fonts/FreeMono.ttf"
numbers_font_size = 25
pos_font = "fonts/FreeMono.ttf"
pos_font_size = 20

def avg(l):
	if len(l) == 0: return 0
	for x in l:
		if not str(x).isdigit(): return float("inf")
	return 1.0*sum(l)/len(l)

def list_2_image(names, l):

	lines = len(l)

	# make sure everything works
	assert lines > 0, "Your list must contain elements."
	assert lines == len(names), "We must have scores for each competitor."
	
	cols = len(l[0])
	for x in l:
		assert len(x) == cols > 0, "At least one of the lines has different column numbers."
	
	data = pd.DataFrame({})
	data["names"] = names
	for i in range(cols):
		data["t%s"%(i+1)] = [x[i] for x in l]
	data["avg"] = [avg([a, b, c]) for a, b, c in zip(data["t1"], data["t2"], data["t3"])]
	data["min"] = [min([	a if str(a).isdigit() else float("inf"),
							b if str(b).isdigit() else float("inf"),
							c if str(c).isdigit() else float("inf")]) for a, b, c in zip(data["t1"], data["t2"], data["t3"])] # for sorting only
	data.sort_values(by = ["avg", "min"], ascending = True, inplace = True)
	data.index = range(len(l))
	
	width = 900
	height = 1080
	
	img = Image.new('RGB', (width, height), color = WHITE)
	
	names_width = width/2
	pos_width = 40
	avg_width = 100
	cell_height = 1.0*height/(len(l)+2)
	cell_width = 1.0*(width-names_width-pos_width-avg_width)/cols
	
	widths = [pos_width, names_width]
	for i in range(cols):
		widths.append(cell_width)
	widths.append(avg_width)

	draw = ImageDraw.Draw(img)
	
	# draw header
	header = ["Pos", "Names", "T1", "T2", "T3", "Avg"]
	fnt = ImageFont.truetype(header_font, header_font_size)
	for i in range(len(widths)):
	
		# centering
		rendered_width, rendered_height = fnt.getsize(header[i])
		x_offset = (widths[i]-rendered_width)/2
		y_offset = (cell_height-rendered_height)/2
		
		draw.text((x_offset + sum(widths[:i]), y_offset), header[i], fill=BLACK, font = fnt)
	
	# draw pos
	pos = 1
	fnt = ImageFont.truetype(numbers_font, pos_font_size)
	for i in range(lines):
	
		temp = str(pos)
		if i != 0 and ((data["avg"])[i] == (data["avg"])[i-1] and (data["min"])[i] == (data["min"])[i-1]):
			temp = "-"
		
		rendered_width, rendered_height = fnt.getsize(temp)
		
		x_offset = (pos_width-rendered_width)/2
		y_offset = (cell_height-rendered_height)/2
			
		draw.text((x_offset, (i+1)*cell_height + y_offset), temp, fill=BLACK, font = fnt)
		
		pos += 1
	
	# draw names
	for i in range(lines):
		temp = (data["names"])[i]
		
		temp_size = names_font_size
		fnt = ImageFont.truetype(names_font, temp_size)
		rendered_width, rendered_height = fnt.getsize(temp)
		
		while rendered_width >= names_width:
			temp_size -= 1
			fnt = ImageFont.truetype(names_font, temp_size)
			rendered_width, rendered_height = fnt.getsize(temp)

		x_offset = (names_width-rendered_width)/2
		y_offset = (cell_height-rendered_height)/2
			
		draw.text((pos_width + x_offset, (i+1)*cell_height + y_offset), temp, fill=BLACK, font = fnt)

	# color for podium
	sorted_attempts = [	sorted(list(set([x if str(x).isdigit() else float("inf") for x in data["t1"]]))),
						sorted(list(set([x if str(x).isdigit() else float("inf") for x in data["t2"]]))),
						sorted(list(set([x if str(x).isdigit() else float("inf") for x in data["t3"]])))]

	# draw numbers and fill rect
	fnt = ImageFont.truetype(numbers_font, numbers_font_size)
	for i in range(lines):
		for j in range(cols):
			
			number = (data["t%s"%(j+1)])[i]
			
			woaj_index = sorted_attempts[j].index(number if str(number).isdigit() else float("inf"))
			if woaj_index < 3:
				draw.rectangle([pos_width + names_width + j*cell_width, (i+1)*cell_height, pos_width + names_width + (j+1)*cell_width, (i+2)*cell_height], fill=WOAJ_COLOR[woaj_index])
			
			number = str(number)
			
			rendered_width, rendered_height = fnt.getsize(number)
			x_offset = (cell_width-rendered_width)/2
			y_offset = (cell_height-rendered_height)/2
			
			draw.text((pos_width + names_width + j*cell_width + x_offset, (i+1)*cell_height + y_offset), number, fill=BLACK, font = fnt)
	
	# draw avg
	fnt = ImageFont.truetype(numbers_font, numbers_font_size)
	for i in range(len(data["avg"])):
			
		temp = "%.2f"%data["avg"][i] if data["avg"][i] != float("inf") else "DNF"
		
		rendered_width, rendered_height = fnt.getsize(temp)
		x_offset = (avg_width-rendered_width)/2
		y_offset = (cell_height-rendered_height)/2
			
		draw.text((sum(widths[:-1]) + x_offset, (i+1)*cell_height + y_offset), temp, fill=BLACK, font = fnt)
	
	# draw woaj
	woajs = [x[0] for x in sorted_attempts] # singles
	woaj = ["", "woaj"] # as rendered
	for x in woajs: woaj.append(x)
	woaj.append("%.2f"%avg(woajs))
	for i in range(len(woaj)):
	
		rendered_width, rendered_height = fnt.getsize(str(woaj[i]))
		x_offset = (widths[i]-rendered_width)/2
		y_offset = (cell_height-rendered_height)/2
		
		draw.text((sum(widths[:i]) + x_offset, cell_height*(len(l)+1) + y_offset), str(woaj[i]), fill=BLACK, font = fnt)
		
	# draw horizontal lines
	for i in range(len(l)+2):
		draw.line([0, i*cell_height, width, i*cell_height], fill = BLACK)
	
	# draw vertical lines
	for i in range(len(widths)):
		draw.line([widths[i]+sum(widths[:i]), 0, widths[i]+sum(widths[:i]), height], fill = BLACK)
	
	return img

def main():
	scores = random_scores()
	names = random_names()
	
	img = list_2_image(names, scores)
	img.save('image.png')	

main()

