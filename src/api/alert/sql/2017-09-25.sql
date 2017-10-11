ALTER TABLE `alpha`.`user`
ADD COLUMN `visit_time` BIGINT(20) NOT NULL DEFAULT 0 AFTER `is_active`,
ADD COLUMN `victor_number` INT NOT NULL DEFAULT 0 AFTER `visit_time`,
ADD COLUMN `fail_number` INT NOT NULL DEFAULT 0 AFTER `victor_number`,
ADD COLUMN `win_percent` DECIMAL(10,2) NOT NULL DEFAULT 0 AFTER `fail_number`,
ADD COLUMN `part_number` INT NOT NULL DEFAULT 0 AFTER `win_percent`;
ADD COLUMN `ranking` INT NULL DEFAULT 0 AFTER `part_number`;