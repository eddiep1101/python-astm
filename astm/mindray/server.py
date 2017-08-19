# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

"""

``astm.mindray.server`` - Server implementation for Mindray
----------------------------------------------------------

"""

from astm.server import BaseRecordsDispatcher
from astm.mapping import (
    Component, ConstantField, ComponentField, RepeatedComponentField, DateTimeField, IntegerField,
    SetField, TextField, NotUsedField, DateField, DecimalField
)
from .common import (
    Header, Terminator,
    CommonPatient,
    CommonOrder,
    CommonResult,
    CommonComment,
    UserName,
    PatientBirthAge,
    QueryRecord
)


__all__ = ['RecordsDispatcher',
           'Header', 'Patient', 'Order', 'Result', 'Query', 'Terminator',
           'Instrument', 'Test', 'Specimen', 'TestType', 'Sample', 'QcInfo', 'ResultValue', 'ResultRange']

#: Specimen information structure.
#:
#: :param patient_id: 病人ID. Length: 30
#: :type patient_id: str
#:
#: :param barcode: 样本条码. Length: 27
#: :type barcode: str
#:

Specimen = Component.build(
    TextField(name='patient_id', length=30),
    TextField(name='barcode', length=27)
)

#: Instrument (analyser) information structure.
#:
#: :param name: 消息发送者. Length: 16
#: :type name: str
#:
#: :param device_id: 设备ID. Length: 10
#: :type device_id: integer
#:
Instrument = Component.build(
    TextField(name='name', length=16),
    IntegerField(name='device_id', length=10)
)

#: Test :class:`~astm.mapping.Component`
#:
#: :param assay_code: 项目通道号 Required. Length: 10
#: :type assay_code: str
#:
#: :param assay_name: 项目名称（全称） Length: 50
#: :type assay_name: str
#:
#: :param dilution: 稀释倍数（保留） Length: 4
#: :type dilution: integer
#:
#: :param repeat: 重复测试次数（保留） Length: 2
#: :type dilution: integer
#:
Test = Component.build(
    TextField(name='assay_code', required=True, length=10),#项目通道号
    TextField(name='assay_name', length=50),#项目名称（全称）
    NotUsedField(name='dilution'),
    NotUsedField(name='repeat')
)

#: TestType :class:`~astm.mapping.Component`
#:
#: :param assay_code: 项目通道号 Required. Length: 10
#: :type assay_code: str
#:
#: :param assay_name: 项目名称（全称） Length: 50
#: :type assay_name: str
#:
#: :param replicate: 结果重复次数编号（保留） Length: 2
#: :type dilution: integer
#:
#: :param result_type: 结果类型 Length: 1, I（定性结果）、F（定量结果）
#: :type dilution: integer
#:
TestType = Component.build(
    TextField(name='assay_code', required=True, length=10),#项目通道号
    TextField(name='assay_name', length=50),#项目名称（全称）
    NotUsedField(name='replicate'),
    SetField(name='result_type', values=('I', 'F'))
)

#: Sample :class:`~astm.mapping.Component`.
#:
#: :param sample_id: 样本ID （如空为质控）. Length: 10
#: :type assay_code: str
#:
#: :param tray_no: （保留） Length: 2
#: :type assay_name: integer
#:
#: :param position: （保留） Length: 2
#: :type dilution: integer
#:
Sample = Component.build(
    TextField(name='sample_id', length=10),
    NotUsedField(name='tray_no'),
    NotUsedField(name='position')
)

#: QcInfo :class:`~astm.mapping.Component`.
#:
#: :param qc_no: 质控液编号. Length: 3
#: :type qc_no: str
#:
#: :param qc_name: 质控液名称. Length: 15
#: :type qc_name: str
#:
#: :param qc_batch: 质控液批次. Length: 18
#: :type qc_batch: str
#:
#: :param qc_expiry: 质控液有效期. Length: 8
#: :type qc_name: Datefield
#:
#: :param qc_avg_value: 质控液均值. Length: 8
#: :type qc_name: integer
#:
#: :param qc_stdev: 质控液标准差. Length: 8
#: :type qc_name: integer
#:
#: :param qc_value: 质控液结果值. Length: 8
#: :type qc_name: integer
#:
QcInfo = Component.build(
    TextField(name='qc_no', length=3),
    TextField(name='qc_name', length=15),
    TextField(name='qc_batch', length=18),
    DateField(name='qc_expiry'),
    IntegerField(name='qc_avg_value', length=8),
    IntegerField(name='qc_stdev', length=8),
    IntegerField(name='qc_value', length=8)
)

#: ResultValue :class:`~astm.mapping.Component`.
#:
#: :param value: 定量值. (Length: 25)
#: :type qc_no: decimal
#:
#: :param interpretation: 字符串（阴性(-)、阳性 (+)、 弱阳性 (+-)等. Length: 10
#: :type qc_name: str
#:
#: :param value_L: 浊度（保留）. Length: 25
#: :type qc_batch: integer
#:
#: :param value_H: 溶血（保留）. Length: 25
#: :type qc_name: integer
#:
#: :param value_I: 黄疸（保留）. Length: 25
#: :type qc_name: integer
#:
ResultValue = Component.build(
    DecimalField(name='value'),
    TextField(name='interpretation', length=10),
    NotUsedField(name='value_L'),
    NotUsedField(name='value_H'),
    NotUsedField(name='value_I')
)

#: ResultRange :class:`~astm.mapping.Component`.
#:
#: :param upper: 参考范围上限. Length: 12
#: :type upper: integer
#:
#: :param lower: 参考范围下限. Length: 12
#: :type lower: integer
#:
ResultRange = Component.build(
    IntegerField(name='upper', length=12),
    IntegerField(name='lower', length=12)
)


class Patient(CommonPatient):
    """ASTM patient record.

    :param type: Record Type ID. Always ``P``.
    :type type: str

    :param seq: Sequence Number. Required.
    :type seq: int

    :param practice_id: Practice Assigned Patient ID. (保留）
    :type practice_id: None

    :param laboratory_id: 病人ID. Required. Length: 30
    :type laboratory_id: str

    :param id: Patient ID. Not used.
    :type id: None

    :param name: Patient name. Required
    :type name: :class:`UserName`

    :param maiden_name: Mother’s Maiden Name. Not used.
    :type maiden_name: None

    :param birthdate: Birthdate.
    :type birthdate: PatientBirthAge

    :param sex: Patient Sex. One of: ``M`` (male), ``F`` (female),
                ``I`` (animal), ``U`` is unknown.
    :type sex: str

    :param race: Patient Race-Ethnic Origin. Not used.
    :type race: None

    :param address: 送检科室. Length: 20
    :type address: str

    :param reserved: Reserved Field. Not used.
    :type reserved: None

    :param phone: Patient Telephone Number. Not used.
    :type phone: None

    :param physician_id: Attending Physician. Not used.
    :type physician_id: None

    :param special_1: Special Field #1. Not used.
    :type special_1: None

    :param special_2: Patient source. （保留）
    :type special_2: None

    :param height: Patient Height. Not used.
    :type height: None

    :param weight: Patient Weight. Not used.
    :type weight: None

    :param diagnosis: 临床诊断. Length: 50
    :type diagnosis: str

    :param medications: Patient’s Active Medications. Not used.
    :type medications: None

    :param diet: Patient’s Diet. Not used.
    :type diet: None

    :param practice_1: Practice Field No. 1. Not used.
    :type practice_1: None

    :param practice_2: Practice Field No. 2. Not used.
    :type practice_2: None

    :param admission_date: Admission/Discharge Dates. Not used.
    :type admission_date: None

    :param admission_status: Admission Status. Not used.
    :type admission_status: None

    :param location: Patient location. （保留）
    :type location: None

    :param diagnostic_code_nature: Nature of diagnostic code. Not used.
    :type diagnostic_code_nature: None

    :param diagnostic_code: Diagnostic code. Not used.
    :type diagnostic_code: None

    :param religion: Patient religion. Not used.
    :type religion: None

    :param martial_status: Martian status. Not used.
    :type martial_status: None

    :param isolation_status: Isolation status. Not used.
    :type isolation_status: None

    :param language: Language. Not used.
    :type language: None

    :param hospital_service: Hospital service. Not used.
    :type hospital_service: None

    :param hospital_institution: Hospital institution. Not used.
    :type hospital_institution: None

    :param dosage_category: Dosage category. Not used.
    :type dosage_category: None
    """
    practice_id = NotUsedField()
    laboratory_id = TextField(length=30)
    name = ComponentField(UserName)
    birthdate = ComponentField(PatientBirthAge)
    address = TextField(length=20)
    special_2 = NotUsedField()
    diagnosis = TextField(length=50)
    location = NotUsedField()
    sex = SetField(default='U', values=('M', 'F', 'U', 'I'))


class Order(CommonOrder):
    """ASTM order record.

    :param type: Record Type ID. Always ``O``.
    :type type: str

    :param seq: Sequence Number. Required.
    :type seq: int

    :param sample_id: 样本ID, Sample information structure
    :type sample: :class:`Sample`

    :param instrument: 样本条码, Instrument specimen ID. Length: 29
    :type instrument: str

    :param test: Test information structure (aka Universal Test ID).
    :type test: :class:`Test`

    :param priority: Priority flag. Required. Possible values:
                     - ``S``: 急诊; -``R``: 常规.
    :type priority: str

    :param created_at: 样本申请时间.
    :type created_at: datetime.datetime

    :param sampled_at: 样本采集时间.
    :type sampled_at: datetime.datetime

    :param collected_at: Collection end time. Not used.
    :type collected_at: None

    :param volume: Collection volume. Not used.
    :type volume: None

    :param collector: Collector ID. Not used.
    :type collector: None

    :param action_code: 质控液信息;
    :type action_code: QcInfo

    :param danger_code: Danger code. Not used.
    :type danger_code: None

    :param clinical_info: Revelant clinical info. Not used.
    :type clinical_info: None

    :param delivered_at: 送检时间.
    :type delivered_at: datetime.datetime

    :param biomaterial: 样本类型，需注意大小写敏感. Length: 20.
    :type biomaterial: str（serum, urine, plasma, timed, other, blood, amniotic）

    :param physician: 送检医生.
    :type physician: :class:`UserName`

    :param physician_phone: 送检科室
    :type physician_phone: str

    :param user_field_1: Offline dilution factor（保留）. Length: 4
    :type user_field_1: integer

    :param user_field_2: 检验医生.
    :type user_field_2: :class:`UserName`

    :param laboratory_field_1: Laboratory field #1. Not used.
    :type laboratory_field_1: None

    :param laboratory_field_2: Laboratory field #2. Not used.
    :type laboratory_field_2: None

    :param modified_at: Date and time of last result modification. Not used.
    :type modified_at: None

    :param instrument_charge: Instrument charge to computer system. Not used.
    :type instrument_charge: None

    :param instrument_section: Instrument section id. Not used.
    :type instrument_section: None

    :param report_type: 报告类型. O（来自LIS的请求）、Q（查询响应）、F（最终的结果）、X（质控：样本被拒绝）
    :type report_type: str

    :param reserved: Reserved. Not used.
    :type reserved: None

    :param location_ward: Location ward of specimen collection. Not used.
    :type location_ward: None

    :param infection_flag: Nosocomial infection flag. Not used.
    :type infection_flag: None

    :param specimen_service: Specimen service. Not used.
    :type specimen_service: None

    :param laboratory: Production laboratory. Not used.
    :type laboratory: None
    """
    sample_id = ComponentField(Sample)
    instrument = TextField(length=29)
    test = RepeatedComponentField(Test)
    created_at = DateTimeField()
    sampled_at = DateTimeField()
    action_code = ComponentField(QcInfo)
    physician = ComponentField(UserName)
    physician_phone = TextField(length=20)
    user_field_1 = NotUsedField()
    user_field_2 = ComponentField(UserName)
    laboratory_field_2 = NotUsedField()
    report_type = SetField(default='F', values=('O', 'Q', 'F', 'X'))


class Result(CommonResult):
    """ASTM result record.

    :param type: Record Type ID. Always ``R``.
    :type type: str

    :param seq: Sequence Number. Required.
    :type seq: int

    :param test: Test information structure
    :type test: :class:`TestType`

    :param value: Measurement value.
    :type value: class: 'ResultValue'

    :param units: Units. Length: 12
    :type units: str

    :param references: Normal reference value interval.
    :type references: class 'ResultRange'

    :param abnormal_flag: Result abnormal flag. Possible values:
                          - ``L``: ( 结果 < 参考范围 );
                          - ``H``: ( 结果 > 参考范围 );
                          - ``N``: ( 正常 );
                          Length: 1.
    :type abnormal_flag: str

    :param abnormality_nature: Nature of abnormality testing. Length: 10
    :type abnormality_nature: str

    :param status: Result status. ``F`` indicates a final result;
                   ``R`` indicating rerun. Length: 1.
    :type status: str

    :param normatives_changed_at: 原始测试结果
    :type normatives_changed_at: class 'ResultRange'

    :param operator: 重测结果标记. Length: 1, 1(重测结果)、0（非重测结果）
    :type operator: integer

    :param started_at: When works on test was started on.
    :type started_at: datetime.datetime

    :param completed_at: When works on test was done.
    :type completed_at: datetime.datetime

    :param instrument: Instrument ID. Required.
    :type instrument: :class:`Instrument`
    """
    test = ComponentField(TestType)
    value = ComponentField(ResultValue)
    units = TextField(length=12)
    references = ComponentField(ResultRange)
    abnormal_flag = SetField(values=('N', 'L', 'H'))
    abnormality_nature = TextField(length = 10)
    status = SetField(values=('F', 'R'))
    normatives_changed_at = ComponentField(ResultValue)
    operator = SetField(values=(0, 1))
    started_at = DateTimeField()
    completed_at = DateTimeField()
    instrument = ComponentField(Instrument)


class Comment(CommonComment):
    """ASTM comment record.

    :param type: Record Type ID. Always ``C``.
    :type type: str

    :param seq: Sequence Number. Required.
    :type seq: int

    :param source: Comment source. Always ``I``.
    :type source: str

    :param data: free text value. Length: 90.
    :type data: str

    :param ctype: 注释类型. Length: 1, G(结果注释)、I(异常字符串)
    :type ctype: str
    """
    source = ConstantField(default = 'I')
    data = TextField(length = 90)
    ctype = SetField(values=('G', 'I'))


class Query(QueryRecord):
    """ASTM query record.

    :param type: Record Type ID. Always ``Q``.
    :type type: str

    :param seq: Sequence Number.
    :type seq: int

    :param specimen: 病人ID及样本条码.
    :type specimen: class 'Specimen'

    :param range_start: 样本起始编号 Length: 20
    :type range_start: str

    :param range_end: 样本终止编号 Length: 20
    :type range_end: str

    :param time_limits: 保留

    :param period_start: 查询起始时间 Length: 14
    :type period_start: datetime

    :param period_end: 查询截止时间 Length: 14
    :type period_end: datetime

    :param physician_name: 保留

    :param physician_phone: 保留

    :param user_field_1: 保留

    :param user_field_2: 保留

    :param status_code: 查询命令码. Length: 1, Ｏ：请求样本查询, A: 取消查询
    :type status_code: str
    """
    specimen = ComponentField(Specimen)
    range_start = TextField(length = 20)
    range_end = TextField(length = 20)
    period_start = DateTimeField()
    period_end = DateTimeField()
    status_code = TextField(length = 1, required = True)


class RecordsDispatcher(BaseRecordsDispatcher):
    """Omnilab specific records dispatcher. Automatically wraps records by
    related mappings."""
    def __init__(self, *args, **kwargs):
        super(RecordsDispatcher, self).__init__(*args, **kwargs)
        self.wrappers = {
            'H': Header,
            'P': Patient,
            'O': Order,
            'R': Result,
            'C': Comment,
            'Q': Query,
            'L': Terminator
        }
