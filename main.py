import cv2
import mediapipe as mp

import time

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import mouse as mouse_get
from pynput.mouse import Button, Controller
# Face mesh detection
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh


drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

mouse = Controller()
#PYGAME INIT
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

#OPENGL INIT
gluPerspective(45, (display[0]/display[1]), 1, 1000.0)
glTranslatef(16, 20, -25)
glRotatef(180, 0, 0, 1)
glEnable(GL_DEPTH_TEST)

# 
# vertices = 	[
# 	[ 0.5, 	-0.5,	-0.5],
# 	[ 0.5, 	 0.5,	-0.5],
# 	[-0.5, 	 0.5,	-0.5],
# 	[-0.5,	-0.5,	-0.5],
# 	[ 0.5,	-0.5,	0.5],
# 	[ 0.5, 	 0.5,	0.5],
# 	[-0.5,	-0.5,	0.5],
# 	[-0.5,	 0.5,	0.5]
# 			]
# edges_axis = (
# 	(2,3),
# 	(3,2)
# 			)
# vert_axis = (
# 	(-10,   0,   0),
# 	( 10,   0,   0),
# 	(  0, -10,   0),
# 	(  0,  10,   0),
# 	(  0,   0, -10),
# 	(  0,   0,  10)
# 			)

clock = pygame.time.Clock()
mouse_pos_x = 990
mouse_pos_y = 540
entrecejo = 9
nariz = 5

with mp_face_mesh.FaceMesh(    min_detection_confidence=0.5,    min_tracking_confidence=0.5) as face_mesh:

	index = 0;
	while cap.isOpened():
		#time.sleep(.5)
		#DRAW WORLD
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glClearColor(0.2, 0.2, 0.2, 1)

		key_W_pressed = False
		key_A_pressed = False
		key_S_pressed = False
		key_D_pressed = False
		key_Q_pressed = False
		key_E_pressed = False
		mov_speed = 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == KEYDOWN:
				if event.key == pygame.K_w: key_W_pressed = True
				if event.key == pygame.K_a: key_A_pressed = True
				if event.key == pygame.K_s: key_S_pressed = True
				if event.key == pygame.K_d: key_D_pressed = True
				if event.key == pygame.K_q: key_Q_pressed = True
				if event.key == pygame.K_e: key_E_pressed = True
			if event.type == KEYUP:
					if event.key == pygame.K_w: key_W_pressed = False
					if event.key == pygame.K_a: key_A_pressed = False
					if event.key == pygame.K_s: key_S_pressed = False
					if event.key == pygame.K_d: key_D_pressed = False
					if event.key == pygame.K_q: key_Q_pressed = False
					if event.key == pygame.K_e: key_E_pressed = False
		if key_W_pressed: glTranslatef(0, -mov_speed, 0)
		if key_S_pressed: glTranslatef(0, mov_speed, 0)
		if key_A_pressed: glTranslatef(mov_speed, 0, 0)
		if key_D_pressed: glTranslatef(-mov_speed, 0, 0)
		if key_Q_pressed: glTranslatef(0, 0, mov_speed*4)
		if key_E_pressed: glTranslatef(0, 0, -mov_speed*4)

		keypoints = []

		success, image = cap.read()
		start = time.time()
		image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
		image.flags.writeable = False
		results = face_mesh.process(image)
		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

		if results.multi_face_landmarks:

			index+=1
			for face_landmarks in results.multi_face_landmarks:
				for data_point in face_landmarks.landmark:
					keypoints.append({
						'X': data_point.x,
						'Y': data_point.y,
						'Z': data_point.z,
						'Visibility': data_point.visibility,
					})
			

			
			glPushMatrix()

			
			glLineWidth(3);
			glColor3fv((1,1,1))
			dot_index=0;
			vertex_nose = (0,0,0)

			total_x = 0;
			total_y = 0;


			for edge in keypoints:

				glBegin(GL_LINES)
				dot_index+=1
				x = float(edge["X"])*30
				y = float(edge["Y"])*30
				z = float(edge["Z"])*30
				vertex1 = (x,y,z)
				total_x+=x;
				total_y+=y;
				if nariz==dot_index:
					
					vertex_nose = vertex1
					vertex2 = (x,y,z+1)
				else :
					vertex2 = (x,y,z+1)
				glVertex3fv( vertex1 )
				glVertex3fv( vertex2 )
				glEnd()

			glPopMatrix()

			# MEDIA
			media_x = total_x/dot_index;
			media_y = total_y/dot_index;
			
			media_z = 0;

			# 
			vertex_media = (media_x,media_y,0)
			vertex_media = (vertex_media[0],vertex_media[1],0)

			diff_x = vertex_nose[0]-vertex_media[0]
			diff_y = vertex_nose[1]-vertex_media[1]


			
			'''diff_x*=10
			diff_y*=10'''
			diff_x = round(diff_x,2)
			diff_y = round(diff_y,2)
			
			diff_x+=1
			diff_x/=2
			diff_x*=1920
			diff_y+=1
			diff_y/=2
			diff_y*=1080
				
			#print(diff_x,diff_y)
			
			speed = 30
			sensitivity = 30
			if diff_x > mouse_pos_x+sensitivity:
				if diff_x > mouse_pos_x: mouse_pos_x+=speed
			if diff_x < mouse_pos_x-sensitivity:
				if diff_x < mouse_pos_x: mouse_pos_x-=speed

			if diff_y > mouse_pos_y+sensitivity:
				if diff_y > mouse_pos_y: mouse_pos_y+=speed
			if diff_y < mouse_pos_y-sensitivity:
				if diff_y < mouse_pos_y: mouse_pos_y-=speed

			# MOVER RATON
			mouse.position = (mouse_pos_x,mouse_pos_y)

			# x0 ==> x0
			# y0 ==> y0
			# x10 ==> x0
			# y0 ==> y0

			# Y == ARRIBA ABAJO
			# -1Y == ABAJO DEL TODO      -1Y ==> 1080Y    0=0 1=1080 .5=540
			# 1Y == ARRIBA DEL TODO       1Y ==> 0Y
			# X == ARRIBA ABAJO
			# -1X == IZQUIERDA DEL TODO  -1X ==> 0X
			# 1X == DERECHA DEL TODO	  1X ==> 1920X

			glBegin(GL_LINES)
			glColor3fv((0,1,0))
			glVertex3fv( vertex_media )
			glVertex3fv( vertex_nose )
			glEnd()



		pygame.display.flip()
		clock.tick(60)


		end = time.time()
		totalTime = end - start
		fps = 1 / totalTime


		if cv2.waitKey(20) & 0xFF == ord('q'):
			break

cap.release()