#!/usr/bin/perl -w
#
#  Copyright 2006 Corey Goldberg (corey@goldb.org)
#
#
#  remote data backup with ssh and ftp
#
#  Usage:
#  remotebackup.pl -r remote_host -u user_name -p password -l backup_list [-d dump_db_boolean]
#
#  
#  
#  This is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This is distributed in the hope that it will be useful,
#  but without any warranty; without even the implied warranty of
#  merchantability or fitness for a particular purpose.  See the
#  GNU General Public License for more details.




use strict;
use Net::FTP;
use Net::SSH::Perl;
use Getopt::Long;
$| = 1;  # don't buffer stdout



my $dump_mysql = 0;  # enable database backup
my $mysql_root_password = "";
my ($host, $user, $pass, $backup_list);  # set from the commandline via getoptions()

getoptions();  # get command line options

my $backup_name = $host . "_" .datetime() . ".tar.gz";  # name of the backup tarball

print "starting remote backup.  $host  ", datetime(), "\n";

print "uploading backup list to remote host... ";
ftp("put", $backup_list);
print "done\n";

print "logging in to remote host... ";
my $ssh = Net::SSH::Perl->new($host);
$ssh->login($user, $pass);
print "done\n";

if ($dump_mysql) {
    print "dumping databases to flat file... ";
    # run mysqldump to dump database tables out to flat files for backup
    command_remote("mysqldump --opt --user=root --password=$mysql_root_password --all-databases > /tmp/db_dump.txt");
    print "done\n";
}

print "creating archive on remote host... ";
command_remote("tar czvf $backup_name -T $backup_list \&> /dev/null");
print "done\n";

print "downloading archive from remote host... ";
ftp("get", $backup_name);
print "done\n";

print "deleting backup list from remote host... ";
command_remote("rm $backup_list");
print "done\n";

if ($dump_mysql) {
    print "deleting database dump from remote host... ";
    #command_remote("rm /tmp/db_dump.txt");
    print "done\n";
}

print "deleting archive from remote host... ";
command_remote("rm $backup_name");
print "done\n";

print "backup complete.\n";



########################## subroutines ##########################

sub command_remote {
    my ($cmd) = @_;
    my ($stdout, $stderr, $exit) = $ssh->cmd($cmd);
    return $stdout;
}



sub datetime {       
    my ($sec, $min, $hour, $day, $month, $year) = (localtime)[0, 1, 2, 3, 4, 5];    
    my $datetime = sprintf "%02d-%02d-%02d-%02d.%02d.%02d", 
      $year + 1900, ($month + 1), $day, $hour, $min, $sec;
    return $datetime;
}



sub ftp {
    my ($method, $file_name) = @_;
    
    my $ftp = Net::FTP->new($host, Debug => 0);
    $ftp->login($user, $pass) or die "ERROR - FTP login failed: ", $ftp->message;
    $ftp->binary;  #switch to binary transfer mode
    
    if ($method eq "put") {
        $ftp->put($file_name) or die "ERROR - FTP put failed: ", $ftp->message;
    }
    elsif ($method eq "get") {
        $ftp->get($file_name) or die "ERROR - FTP get failed: ", $ftp->message;
    }
    
    $ftp->quit;
}



sub getoptions {  # command line options
    Getopt::Long::Configure('bundling');
    GetOptions(
        'r|remotehost=s'    => \$host,
        'u|user=s'          => \$user,
        'p|pass=s'          => \$pass,
        'l|backup_list=s'   => \$backup_list,
        'd|dump_db:i'       => \$dump_mysql,
    ) 
    or do {
        print_usage();
        exit();
    };
    # check for required options
    if (!$host or !$user or !$pass or !$backup_list) {
        print "Invalid options\n";
        print_usage();
        exit(1);
    }
}



sub print_usage {
    print "  Usage:\n";
    print "  remotebackup.pl -r remote_host -u user_name -p password -l backup_list [-d dump_db_boolean]\n ";
}