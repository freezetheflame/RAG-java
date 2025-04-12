from sqlalchemy.engine.result import null_result

from app.core.query.query_construction.entity_expander import EntityExpander


def test_build():
    entity_exbander = EntityExpander()
    #检查字典加载
    assert entity_exbander.synonym_mapping != {}, "entity_dict should not be empty"

    # 测试输入
    query = "介绍一下java中的类"
    #检查实体
    result = entity_exbander.build(query)
    assert result.get("entities")!=null_result(), f"got {result}"
    print(result)