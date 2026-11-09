This project is a rogue-like dungeon crawler game that I made for my A Level Coding project in 2024-2025 under the OCR Computer Science Course, using pygame.

It scored 69/70 marks in the submission, for access to the document that accompanied this code, you'd have to reach out with good justification.

If any issues are experienced with the project you can file it as an issue and it might be addressed.

MichaelFD21 is the only contributor and maintainer of the project, but due to it being my A level project, further features and improvements are unlikely to be published

Modifying the game:
Do note that further modifications to the game was not intended to be done by other users, so modification content and methods may seem limited.

It is possible to change the displayed assets of the map, characters, enemies and projectiles through adding your custom image to the Assets folder and renaming them accordingly. Do note that if you were to use custom assets, it could break the functionality of certain features due to there being no current system to restrict the size of assets to its currently used values.

Additional rooms can be added by using CreateRoom in Rooms.py and specifying the dimensions and tile types.

All of the classes for enemies, projectiles and players can be found in the Classes.py file, you can technically add more enemies and types by modifying that file, but to use it, it would have to be assigned an enemy tier at the bottom of the file so that it can be randomly selected accordingly.