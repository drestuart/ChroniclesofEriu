#!/usr/bin/perl
use 5.010;

$text = `cat places_raw`;

=pod
while ($text =~ m/<tr>\n<td><b>(.+?)<\/b><\/td>/g) {
	$names = $1;

	while ($names =~ m/([A-Za-z'"]+)/g) {
		say $1;
	}
}
=cut

$text =~ s/,\s+/\n/g;
$text =~ s/\(.+?\)//g;
say $text;