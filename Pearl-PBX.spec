Name: Pearl-PBX
Version: 1.0
Release: centos6

Summary: Web GUI for Asterisk written by Alex Radetsky <rad@rad.kiev.ua> 

License: GPL

Group: Networking/Other
Url: http://www.pearlpbx.com/

Packager: Alex Radetsky <rad@rad.kiev.ua>

BuildArch: noarch
Source0: %name-%version.tar

#BuildRequires: make
#BuildRequires: perl-CGI perl-Class-Accessor-Class perl-Config-General perl-DBI perl-Encode perl-FCGI perl-Unix-Syslog
#BuildRequires: perl-NetSDS perl-Class-Accessor-Class perl-Class-Accessor

Requires: asterisk > 11
Requires: asterisk-postgresql
Requires: postgresql-server
Requires: postgresql
Requires: perl-NetSDS
Requires: perl-Class-Accessor-Class 
Requires: perl-Class-Accessor 
Requires: perl-Template-Toolkit 
Requires: perl-NetSDS-Asterisk 
Requires: perl-asterisk-perl 
Requires: httpd 
Requires: asterisk-sounds-ru-wav
Requires: asterisk-sounds-ru-gsm
Requires: asterisk-sounds-ru-alaw
Requires: uuid-pgsql
Requires: perl-CGI-Session
Requires: perl-CGI-Session-Auth
Requires: system-config-network-tui 
Requires: monit 

%description
Web GUI for Asterisk written by Alex Radetsky <rad@rad.kiev.ua>

%prep
%setup -n %name-%version

%build

%install

rm -rf %{buildroot}

mkdir -p %buildroot/var/run/NetSDS
chmod 777 %buildroot/var/run/NetSDS

mkdir -p %buildroot/var/lib/asterisk/agi-bin
install -m 755  agi-bin/NetSDS-AGI-integration.pl %buildroot/var/lib/asterisk/agi-bin
install -m 755  agi-bin/NetSDS-route.pl %buildroot/var/lib/asterisk/agi-bin

mkdir -p %buildroot/usr/bin
mkdir -p %buildroot/usr/sbin
install -D -m 755  bin/* %buildroot/usr/bin/ 
install -D -m 755  sbin/* %buildroot/usr/sbin/

install -d -m 755  %buildroot/etc/NetSDS
install -m 644  etc/NetSDS/asterisk-router.conf %buildroot/etc/NetSDS

install -D -m 644  etc/apache2/sites-available/pearlpbx %buildroot/etc/httpd/conf.d/pearlpbx.conf 

install -d -m 755  %buildroot/etc/monit.d
install -D -m 755  etc/init.d/pearlpbx-parsequeuelogd %buildroot/etc/init.d 
install -D -m 644  etc/monit.d/* %buildroot/etc/monit.d/

install -D -m 755  etc/init.d/pearlpbx-hangupd %buildroot/etc/init.d
install -D -m 755  etc/monit.d/pearlpbx-hangupd %buildroot/etc/monit.d

install -D -m 755  etc/monit.d/asterisk %buildroot/etc/monit.d/

install -d -m 755  %buildroot/etc/cron.d
install -D -m 755  etc/cron.d/* %buildroot/etc/cron.d/ 

install -d -m 755  %buildroot/etc/asterisk
install -D -m 755  etc/asterisk1.8/* %buildroot/etc/asterisk

install -d -m 755  %buildroot/usr/share/perl5
install -D -m 644  lib/*.pm %buildroot/usr/share/perl5/

cp -a lib/PearlPBX %buildroot/usr/share/perl5
cp -a lib/Pearl %buildroot/usr/share/perl5
cp -a lib/NetSDS %buildroot/usr/share/perl5

mkdir -p %buildroot/usr/share/pearlpbx
cp -av share/reports %buildroot/usr/share/pearlpbx/

install -d -m 755  %buildroot/usr/share/asterisk/sounds
cp -av sounds/* %buildroot/usr/share/asterisk/sounds/ 

mkdir -p %buildroot/var/lib/tftpboot
chmod 777 %buildroot/var/lib/tftpboot
cp -a var/lib/tftpboot/* %buildroot/var/lib/tftpboot 

install -D -d -m 755  %buildroot/var/www/pearlpbx 
cp -a web/* %buildroot/var/www/pearlpbx/ 
install -D -m 644  var/lib/pgsql/data/pg_hba.conf %buildroot/var/lib/pgsql/data/pg_hba.conf 

%pre

%post

ln -sf /etc/NetSDS /etc/PearlPBX

chkconfig pearlpbx-parsequeuelogd on
chkconfig pearlpbx-hangupd on 
chkconfig asterisk on 
chkconfig postgresql on 
chkconfig httpd on 
chkconfig monit on 

/usr/sbin/PearlPBX-gui-passwd.pl admin admin 

/etc/init.d/postgresql initdb
/etc/init.d/postgresql start 
psql -U postgres -f sql/create_user_asterisk.sql
psql -U asterisk -f sql/asterisk.sql 
psql -U asterisk -f sql/directions_list.sql
psql -U asterisk -f sql/directions.sql 
psql -U asterisk -f sql/sip_conf.sql 
psql -U asterisk -f sql/extensions_conf.sql 
psql -U asterisk -f sql/route.sql 


%files
%defattr(-,root,root,-)
%doc README* *.txt 

/etc/NetSDS/asterisk-router.conf
/etc/asterisk/cdr_pgsql.conf
/etc/asterisk/extconfig.conf
/etc/asterisk/extensions.conf
/etc/asterisk/features.conf
/etc/asterisk/http.conf
/etc/asterisk/logger.conf
/etc/asterisk/manager.conf
/etc/asterisk/modules.conf
/etc/asterisk/queues.conf
/etc/asterisk/res_pgsql.conf
/etc/asterisk/say.conf
/etc/cron.d/pearlpbx
/etc/httpd/conf.d/pearlpbx.conf
/etc/init.d
/etc/monit.d/asterisk
/etc/monit.d/pearlpbx-hangupd
/etc/monit.d/pearlpbx-parsequeuelogd
/usr/bin/PearlPBX-tftpprovisor.pl
/usr/bin/ffmpeg-any-to-alaw.sh
/usr/bin/grandstream-config.pl
/usr/bin/gspeech.sh
/usr/bin/moh-convert.pl
/usr/bin/permissions.pl
/usr/bin/tftpprovisor.sh
/usr/bin/ulines.pl
/usr/sbin/NetSDS-hangupd.pl
/usr/sbin/NetSDS-parsequeuelogd.pl
/usr/sbin/PearlPBX-gui-passwd.pl
/usr/sbin/PearlPBX-parsequeuelogd.pl
/usr/sbin/PearlPBX-recd.pl
/usr/sbin/missedcallnotification.pl
/usr/sbin/removedublicatefromqueuelog.pl
/usr/share/asterisk/sounds/en/pearlpbx-nomorelines.alaw
/usr/share/asterisk/sounds/en/pearlpbx-nomorelines.mp3
/usr/share/asterisk/sounds/en/pearlpbx-nomorelines.wav
/usr/share/asterisk/sounds/ru/pearlpbx-nomorelines.alaw
/usr/share/asterisk/sounds/ru/pearlpbx-nomorelines.mp3
/usr/share/asterisk/sounds/ru/pearlpbx-nomorelines.wav
/usr/share/pearlpbx/reports/001-alltraffic.html
/usr/share/pearlpbx/reports/002-calls-to-external-extension.html
/usr/share/pearlpbx/reports/003-incoming-from-customer.html
/usr/share/pearlpbx/reports/004-outgoing-to-customer.html
/usr/share/pearlpbx/reports/005-outgoing-made-by-group.html
/usr/share/pearlpbx/reports/006-incoming-to-group.html
/usr/share/pearlpbx/reports/007-outgoing-made-by-operator.html
/usr/share/pearlpbx/reports/008-incoming-to-operator.html
/usr/share/pearlpbx/reports/009-customer.html
/usr/share/pearlpbx/reports/README
/usr/share/pearlpbx/reports/summary/010-sum-calls-to-external-extensions.html
/usr/share/pearlpbx/reports/summary/020-sum-calls-to-groups.html
/usr/share/pearlpbx/reports/summary/030-received-by-operators-in-groups.html
/usr/share/pearlpbx/reports/summary/035-received-by-operators.html
/usr/share/pearlpbx/reports/summary/040-outgoing-by-operators-in-group.html
/usr/share/pearlpbx/reports/summary/045-lost-in-groups.html
/usr/share/pearlpbx/reports/templates/ExternalNumbers.html
/usr/share/pearlpbx/reports/templates/ListChannels.html
/usr/share/pearlpbx/reports/templates/ListQueues.html
/usr/share/pearlpbx/reports/templates/LostInGroups.html
/usr/share/pearlpbx/reports/templates/Makefile
/usr/share/pearlpbx/reports/templates/Recordings.html
/usr/share/pearlpbx/reports/templates/SumCallsToExternalExtensions.html
/usr/share/pearlpbx/reports/templates/SumCallsToGroups.html
/usr/share/pearlpbx/reports/templates/SumOutgoingByOperatorsInGroup.html
/usr/share/pearlpbx/reports/templates/SumReceivedByOperators.html
/usr/share/pearlpbx/reports/templates/SumReceivedByOperatorsInGroup.html
/usr/share/pearlpbx/reports/templates/alltraffic.html
/usr/share/pearlpbx/reports/templates/callsToExternalNumbers.html
/usr/share/pearlpbx/reports/templates/cdrfilter.html
/usr/share/pearlpbx/reports/templates/customer.html
/usr/share/pearlpbx/reports/templates/incomingFromCustomer.html
/usr/share/pearlpbx/reports/templates/incomingToGroup.html
/usr/share/pearlpbx/reports/templates/incomingToOperator.html
/usr/share/pearlpbx/reports/templates/outgoingMadeByGroup.html
/usr/share/pearlpbx/reports/templates/outgoingMadeByOperator.html
/usr/share/pearlpbx/reports/templates/outgoingToCustomer.html
/usr/share/perl5/NetSDS/Util/DateTime.pm
/usr/share/perl5/NetSDS/Util/String.pm
/usr/share/perl5/Pearl.pm
/usr/share/perl5/Pearl/Auth.pm
/usr/share/perl5/Pearl/Session.pm
/usr/share/perl5/PearlPBX/Queues.pm
/usr/share/perl5/PearlPBX/Report.pm
/usr/share/perl5/PearlPBX/Report/ExternalNumbers.pm
/usr/share/perl5/PearlPBX/Report/ListChannels.pm
/usr/share/perl5/PearlPBX/Report/ListQueues.pm
/usr/share/perl5/PearlPBX/Report/LostInGroups.pm
/usr/share/perl5/PearlPBX/Report/Recordings.pm
/usr/share/perl5/PearlPBX/Report/SumCallsToExternalExtensions.pm
/usr/share/perl5/PearlPBX/Report/SumCallsToGroups.pm
/usr/share/perl5/PearlPBX/Report/SumOutgoingByOperatorsInGroup.pm
/usr/share/perl5/PearlPBX/Report/SumReceivedByOperators.pm
/usr/share/perl5/PearlPBX/Report/SumReceivedByOperatorsInGroup.pm
/usr/share/perl5/PearlPBX/Report/alltraffic.pm
/usr/share/perl5/PearlPBX/Report/callsToExternalNumbers.pm
/usr/share/perl5/PearlPBX/Report/cdrfilter.pm
/usr/share/perl5/PearlPBX/Report/customer.pm
/usr/share/perl5/PearlPBX/Report/incomingFromCustomer.pm
/usr/share/perl5/PearlPBX/Report/incomingToGroup.pm
/usr/share/perl5/PearlPBX/Report/incomingToOperator.pm
/usr/share/perl5/PearlPBX/Report/listlostcalls.pm
/usr/share/perl5/PearlPBX/Report/outgoingMadeByGroup.pm
/usr/share/perl5/PearlPBX/Report/outgoingMadeByOperator.pm
/usr/share/perl5/PearlPBX/Report/outgoingToCustomer.pm
/usr/share/perl5/PearlPBX/Route.pm
/usr/share/perl5/PearlPBX/SIP.pm
/var/lib/asterisk/agi-bin/NetSDS-AGI-integration.pl
/var/lib/asterisk/agi-bin/NetSDS-route.pl
/var/lib/pgsql/data/pg_hba.conf
/var/lib/tftpboot/lang/spa502g_en.xml
/var/lib/tftpboot/lang/spa502g_ru.xml
/var/lib/tftpboot/spa502G.cfg
/var/lib/tftpboot/spa502G.xml
/var/lib/tftpboot/spa504G.cfg
/var/lib/tftpboot/spa504G.xml
/var/www/pearlpbx/Makefile
/var/www/pearlpbx/cdr2recordings.pl
/var/www/pearlpbx/css/.DS_Store
/var/www/pearlpbx/css/bootstrap-datepicker.css
/var/www/pearlpbx/css/bootstrap-responsive.css
/var/www/pearlpbx/css/bootstrap-responsive.min.css
/var/www/pearlpbx/css/bootstrap.css
/var/www/pearlpbx/css/bootstrap.min.css
/var/www/pearlpbx/css/pearlpbx.css
/var/www/pearlpbx/img/.DS_Store
/var/www/pearlpbx/img/PearlPBX-logo-icon.gif
/var/www/pearlpbx/img/PearlPBX-logo-icon.ico
/var/www/pearlpbx/img/PearlPBX-logo.PSD
/var/www/pearlpbx/img/PearlPBX-logo.png
/var/www/pearlpbx/img/glyphicons-halflings-white.png
/var/www/pearlpbx/img/glyphicons-halflings.png
/var/www/pearlpbx/img/remove-icon.png
/var/www/pearlpbx/index.html
/var/www/pearlpbx/jPlayer/Jplayer.swf
/var/www/pearlpbx/jPlayer/add-on/jplayer.playlist.min.js
/var/www/pearlpbx/jPlayer/add-on/jquery.jplayer.inspector.js
/var/www/pearlpbx/jPlayer/jquery.jplayer.min.js
/var/www/pearlpbx/jPlayer/skin/blue.monday/jplayer.blue.monday.css
/var/www/pearlpbx/jPlayer/skin/blue.monday/jplayer.blue.monday.jpg
/var/www/pearlpbx/jPlayer/skin/blue.monday/jplayer.blue.monday.seeking.gif
/var/www/pearlpbx/jPlayer/skin/blue.monday/jplayer.blue.monday.video.play.png
/var/www/pearlpbx/jPlayer/skin/pink.flag/jplayer.pink.flag.css
/var/www/pearlpbx/jPlayer/skin/pink.flag/jplayer.pink.flag.jpg
/var/www/pearlpbx/jPlayer/skin/pink.flag/jplayer.pink.flag.seeking.gif
/var/www/pearlpbx/jPlayer/skin/pink.flag/jplayer.pink.flag.video.play.png
/var/www/pearlpbx/js/.DS_Store
/var/www/pearlpbx/js/Makefile
/var/www/pearlpbx/js/astman-jah.js
/var/www/pearlpbx/js/bootstrap-datepicker.js
/var/www/pearlpbx/js/bootstrap.js
/var/www/pearlpbx/js/bootstrap.min.js
/var/www/pearlpbx/js/jqPlot/excanvas.js
/var/www/pearlpbx/js/jqPlot/excanvas.min.js
/var/www/pearlpbx/js/jqPlot/jquery.jqplot.css
/var/www/pearlpbx/js/jqPlot/jquery.jqplot.js
/var/www/pearlpbx/js/jqPlot/jquery.jqplot.min.css
/var/www/pearlpbx/js/jqPlot/jquery.jqplot.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.BezierCurveRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.BezierCurveRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.barRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.barRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.blockRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.blockRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.bubbleRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.bubbleRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.canvasAxisLabelRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.canvasAxisLabelRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.canvasAxisTickRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.canvasAxisTickRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.canvasOverlay.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.canvasOverlay.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.canvasTextRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.canvasTextRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.categoryAxisRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.categoryAxisRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.ciParser.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.ciParser.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.cursor.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.cursor.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.dateAxisRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.dateAxisRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.donutRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.donutRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.dragable.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.dragable.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.enhancedLegendRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.enhancedLegendRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.funnelRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.funnelRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.highlighter.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.highlighter.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.json2.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.json2.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.logAxisRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.logAxisRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.mekkoAxisRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.mekkoAxisRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.mekkoRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.mekkoRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.meterGaugeRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.meterGaugeRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.ohlcRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.ohlcRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pieRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pieRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pointLabels.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pointLabels.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pyramidAxisRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pyramidAxisRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pyramidGridRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pyramidGridRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pyramidRenderer.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.pyramidRenderer.min.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.trendline.js
/var/www/pearlpbx/js/jqPlot/plugins/jqplot.trendline.min.js
/var/www/pearlpbx/js/jquery.js
/var/www/pearlpbx/js/pearlpbx.js
/var/www/pearlpbx/login.html
/var/www/pearlpbx/login.pl
/var/www/pearlpbx/queues.pl
/var/www/pearlpbx/recordings.pl
/var/www/pearlpbx/reports.pl
/var/www/pearlpbx/route.pl
/var/www/pearlpbx/sip.pl
/var/www/pearlpbx/stored_sessions.pl

%changelog
* Wed Feb 27 2013 Alex Radetsky <rad@rad.kiev.ua> 1.0-centos6
- Initial build of Pearl-PBX 1.0 



