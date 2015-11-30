#Test Case for DB Retrieval
#Written in PERL by Ryan Connors

#This script retrieves the results of DB querry and stores the resulting tables in a hashmap.
#It then accepts user qry to verify results were retrieved and stored.

my @results;
my %date_data_map;

#fires off the python command
@results = `python SqlPull.py`;

foreach my $x (@results) {
	my $date;
	my $time;
	my $readings;
	my $temp;

	#output data, as parsing to table
	print $x;

	#some regex, that probably looks nightmarish, but it's just grabing digits
	#and non whitespaces, storing them in 'register' variables and then
	#pushing them to the hashmap, I've stored them in temporary variables
	#purely for readability
	if ($x =~ /readings (\d+),(\d+),(\d+) and (\d+) degrees at (\S+) (\S+)/) {
		$readings = "${1}, ${2}, ${3}";	
		$temp = $4;
		$date = $5;
		$time = $6;
	}
	else {
		next;
	}
	
	#assign the data retrieved to the appropriate date
	$date_data_map{$date."_".$time} = $readings;
	
}

#querry tester for date to check
print "\nEnter Date_Time to querry in format yyyy-mm-dd_hh:mm:ss\n";
$qry = <>;
chomp $qry;

#report results.
if (defined $date_data_map{$qry} ) {
	print $date_data_map{$qry};
}
else {
	print "Unable to find data for this entry, terminating...\n";
}
