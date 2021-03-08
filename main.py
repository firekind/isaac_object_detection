from isaac import Application
from codelets import EdgeDetector

def main():
    app = Application(app_filename="apps/object_detection/graphs/detection.app.json")
    app.nodes["edge_detector.subgraph.edge_detector"].add(EdgeDetector, "detector") 
    app.run()


if __name__ == '__main__':
    main()
