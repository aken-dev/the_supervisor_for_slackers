-- sv_for_slackers.working_record definition

CREATE TABLE `working_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'レコードID',
  `user_id` int(11) NOT NULL COMMENT 'ユーザID',
  `line_user_id` varchar(100) NOT NULL COMMENT 'LINE_USER_ID',
  `process_category` int(11) NOT NULL DEFAULT 1 COMMENT '処理区分（0=メンテ，1=作業記録，2=メモのみ）',
  `process_status` int(11) NOT NULL DEFAULT 0 COMMENT '処理状態（0=メンテ, 1=未開始，2=記録中，3=記録正常終了，4=記録異常終了，5=メモのみ）',
  `stage` int(11) NOT NULL COMMENT '作業番号',
  `start_time` datetime DEFAULT NULL COMMENT '作業開始日時',
  `finish_time` datetime DEFAULT NULL COMMENT '作業終了日時',
  `registered_datetime` datetime DEFAULT NULL COMMENT '登録日時',
  `registered_by` varchar(100) DEFAULT NULL COMMENT '登録機能',
  `updated_datetime` datetime DEFAULT NULL COMMENT '更新日時',
  `updated_by` varchar(100) DEFAULT NULL COMMENT '更新機能',
  `memo_1` varchar(200) DEFAULT NULL COMMENT 'メモ1',
  `memo_2` varchar(200) DEFAULT NULL COMMENT 'メモ2',
  `memo_3` varchar(200) DEFAULT NULL COMMENT 'メモ3',
  `standby_status` int(11) NOT NULL DEFAULT 0 COMMENT '待機状態（0=準備完了，1=バッチ処理中，2=バッチ再計算処理待ち，3=バッチ異常終了）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='作業記録';