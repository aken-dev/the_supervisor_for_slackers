-- sv_for_slackers.user_info definition

CREATE TABLE `user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ユーザID',
  `line_user_id` varchar(100) NOT NULL COMMENT 'LINE_USER_ID',
  `line_name` varchar(100) DEFAULT NULL COMMENT 'LINE_NAME（登録時）',
  `allowed` tinyint(4) NOT NULL COMMENT '0=未登録，1=未許可，2=許可，3=禁止',
  `the_last_stage` int(11) NOT NULL DEFAULT 10 COMMENT '課題最終番号',
  `current_stage` int(11) NOT NULL DEFAULT 1 COMMENT '現在の課題番号',
  `stage_change_remind_type` int(11) NOT NULL DEFAULT 0 COMMENT '課題番号変更リマインド間隔種別（0=しない，1=曜日，2=日数）',
  `stage_change_remind_value` int(11) NOT NULL DEFAULT 0 COMMENT '課題番号変更リマインド間隔（0~6=月〜日曜日 or 日数）',
  `recent_stage_changed_date` date DEFAULT NULL COMMENT '直近課題番号変更日',
  `required_working_hours` int(11) NOT NULL DEFAULT 8 COMMENT '目標作業時間（1日あたり）',
  `starting_time_of_a_day` int(11) NOT NULL DEFAULT 0 COMMENT '日付起算時刻（時）',
  `supervisor_flag` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'システム管理者フラグ',
  `registered_datetime` datetime DEFAULT NULL COMMENT '登録日時',
  `registered_by` varchar(100) DEFAULT NULL COMMENT '登録機能',
  `updated_datetime` datetime DEFAULT NULL COMMENT '更新日時',
  `updated_by` varchar(100) DEFAULT NULL COMMENT '更新機能',
  `memo_1` varchar(200) DEFAULT NULL COMMENT 'メモ1',
  `memo_2` varchar(200) DEFAULT NULL COMMENT 'メモ2',
  `memo_3` varchar(200) DEFAULT NULL COMMENT 'メモ3',
  `standby_status` int(11) NOT NULL DEFAULT 0 COMMENT '待機状態（0=準備完了，1=バッチ処理中，2=バッチ再計算処理待ち，3=バッチ異常終了）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='ユーザ情報';