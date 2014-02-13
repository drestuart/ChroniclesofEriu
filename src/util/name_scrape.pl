#!/usr/bin/perl
use 5.010;

$text = `cat female`;

while ($text =~ m/<tr>\n<td><b>(.+?)<\/b><\/td>/g) {
	$names = $1;

	while ($names =~ m/([A-Za-z'"]+)/g) {
		say $1;
	}
}
