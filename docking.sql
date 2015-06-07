CREATE TABLE IF NOT EXISTS `containers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_team` int(11) NOT NULL,
  `id_host` int(11) NOT NULL,
  `id_docker` int(11) NOT NULL,
  `memory` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `hosts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `ip` varchar(200) NOT NULL,
  `port` int(5) NOT NULL,
  `max_memory` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `login` varchar(200) NOT NULL,
  `passwd` varchar(200) NOT NULL,
  `max_memory` varchar(5) NOT NULL,
  `group` varchar(5) NOT NULL,
  `id_host` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

INSERT INTO `teams` (`id`, `name`, `login`, `passwd`, `max_memory`, `group`, `id_host`) VALUES
(1,'Admins', 'admin', 'admin', '1', '0', '0')
