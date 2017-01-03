create table `peak_intersection`(
  `experiment_idA` varchar(10) NOT NULL,
  `experiment_idB` varchar(10) NOT NULL,
  `jaccard` DECIMAL(8,7) NOT NULL,
  `n_intersections` int(10) NOT NULL,
  `log_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`experiment_idA`, `experiment_idB`)
);
