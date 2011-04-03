$(document).ready(function() {
	// Apply special "first" class to sidebar sections, for spacing
	$("#sidebar ul li ul li:first-child").addClass("first");
	$("#sidebar #menu ul li:first-child").addClass("first");
	// Remove border from last post in index listing
	$("#content .post:last-child .entry").css("border-bottom", "0");
});
