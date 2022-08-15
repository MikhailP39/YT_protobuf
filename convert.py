"""Libraries."""
import messages_pb2 as Request
import messages_pb2 as Response
from google.protobuf.json_format import MessageToDict
from operator import itemgetter


def decode_message(message1=None, message2=None):
    """Get Request message."""
    request = Request.Request()

    """Get Response message."""
    response = Response.Response()

    """Decode messages."""
    request.ParseFromString(message1)
    response.ParseFromString(message2)

    # print(request)
    print(response)
    print("-----------------------")

def get_request(message):
    """Get Request message."""
    request = Request.Request()
    """Decode messages."""
    request.ParseFromString(message)
    """Transform Request message to Dict"""
    dict_request = MessageToDict(request)
    """Create Lists with Steps."""
    list_steps = dict_request['steps']
    """Create Parents, Children and Durations lists."""
    list_parents = []
    list_children = []
    list_durations = []
    """Fill the Parents, Children and Durations lists."""
    for i in range(len(list_steps)):
        dict_item = list_steps[i]
        list_durations.append(dict_item['duration'])
        if dict_item['id'] == dict_request['stepId'] or not dict_item['parentId']:
            list_parents.append(list_steps[i])
        else:
            list_children.append(list_steps[i])
    """Find the Max duration."""
    max_duration = max(list_durations)
    """Sort Children List by the Durations"""
    list_children = sorted(list_children, key=itemgetter('duration'), reverse=True)
    """Sum of the Children Durations by ParentId"""
    children_duration_by_parent = []
    for p in range(len(list_parents)):
        for c in range(len(list_children)):
            children_item = list_children[c]
            parent_item = list_parents[p]
            if children_item['parentId'] == parent_item['id']:
                children_duration_by_parent.append(children_item['duration'])
    sum_children_duration = sum(children_duration_by_parent)

    """Fill the Response message."""
    response = Response.Response()
    parents_response = response.hierarchical_step.add()
    set_response(parents_response, list_parents, list_children, dict_request)
    """Fill the MAX Duration Step Name."""
    for i in range(len(list_steps)):
        dict_item = list_steps[i]
        if dict_item['duration'] == max_duration:
            response.max_duration_step_name = dict_item['name']
    """Fill the MAX Duration Step Duration."""
    response.max_duration_step_duration = max_duration - sum_children_duration
    """Transform Response message to the Bite."""
    message_response = response.SerializeToString()
    """Print the Bite Response Message Result"""
    return message_response
    # print(list_parents)
    # print(list_children)
    # print(list_durations)
    # print(sum_children_duration)
    # print(max_duration)
    # print(response)


def set_response(parent_response, parents, children, dict_request):
    for p in range(len(parents)):
        for c in range(len(children)):
            children_item = children[c]
            parents_item = parents[p]
            if parents_item['id'] == dict_request['stepId'] or not parents_item['parentId']:
                parent_response.name = parents_item['name']
                parent_response.duration = parents_item['duration']
            if children_item['parentId'] == parents_item['id']:
                children_response = parent_response.children.add()
                children_response.name = children_item['name']
                children_response.duration = children_item['duration']
            else:
                children_response_else = children_response.children.add()
                children_response_else.name = children_item['name']
                children_response_else.duration = children_item['duration']


def main():
    request = b'\n\x08\x08\x01\x18\x96\x01"\x01A\n\t\x08\x02\x10\x01\x18-"\x01B\n\t\x08\x03\x10\x01\x182"\x01C\n\t\x08\x04\x10\x02\x18\x14"\x01D\n\t\x08\x05\x10\x02\x18\x14"\x01E\x10\x01'
    # response = b'\n"\n\x01A\x10\x96\x01\x1a\x05\n\x01C\x102\x1a\x13\n\x01B\x10-\x1a\x05\n\x01D\x10\x14\x1a\x05\n\x01E\x10\x14\x12\x01A\x187'
    # decode_message(request, response)
    response = get_request(request)

    print(f"Your request message: {request}")
    print(f"After transform request to response: {response}")


if __name__ == "__main__":
    main()