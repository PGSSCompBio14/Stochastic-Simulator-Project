<html>

	<head>
	  <title>Filesystem</title>
	</head>
	
	<body>
	  <?php
	  // Find and write properties
	  echo "<h1>file: lesson14.php</h1>";
	  echo "<p>Was last edited: " . date("r", filemtime("test.php")); 
	  echo "<p>Was last opened: " . date("r", fileatime("test.php")); 
	  echo "<p>Size: " . filesize("test.php") . " bytes";
	  ?>
	</body>
	
</html>
