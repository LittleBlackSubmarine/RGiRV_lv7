import vtk
from time import process_time


iterations = [10, 50, 100, 500, 1000]
landmarks = [10, 50, 100, 500, 1000]

n = 0
while n < 1 or n > 5:
    n = int(input("Choose bunny model to transform[1-5]: "))

target_path = "./3D modeli/bunny.ply"
source_path = "./3D modeli/bunny_t" + str(n) + ".ply"

first = True

print("\nExit windows using 'X' in right top corner or using 'q' button\n")
print("\n CLOSE THE SOURCE WINDOW FIRST!\n")

for iteration in iterations:
    for landmark in landmarks:



        # Source and target renderers
        renderer_t = vtk.vtkRenderer()
        renderer_s = vtk.vtkRenderer()

        # White background
        renderer_t.SetBackground(1, 1, 1)
        renderer_s.SetBackground(1, 1, 1)

        # Source and target rendering windows
        window_t = vtk.vtkRenderWindow()
        window_t.AddRenderer(renderer_t)
        window_t.SetSize(700, 480)
        window_t.SetWindowName("Target")

        window_s = vtk.vtkRenderWindow()
        window_s.AddRenderer(renderer_s)
        window_s.SetSize(700, 480)
        window_s.SetWindowName("Source")

        window_t_interactor = vtk.vtkRenderWindowInteractor()
        window_t_interactor.SetRenderWindow(window_t)

        window_s_interactor = vtk.vtkRenderWindowInteractor()
        window_s_interactor.SetRenderWindow(window_s)

        # Reading .ply model data
        reader_t = vtk.vtkPLYReader()
        reader_t.SetFileName(target_path)
        reader_t.Update()
        data_t = reader_t.GetOutput()

        reader_s = vtk.vtkPLYReader()
        reader_s.SetFileName(source_path)
        reader_s.Update()
        data_s = reader_s.GetOutput()

        # Mapping
        mapper_s = vtk.vtkPolyDataMapper()
        mapper_s.SetInputData(data_s)
        actor_s = vtk.vtkActor()
        actor_s.SetMapper(mapper_s)
        actor_s.GetProperty().SetColor(0, 1, 0)
        renderer_s.AddActor(actor_s)

        mapper_t = vtk.vtkPolyDataMapper()
        mapper_t.SetInputData(data_t)
        actor_t = vtk.vtkActor()
        actor_t.SetMapper(mapper_t)
        actor_t.GetProperty().SetColor(1, 0, 0)
        #renderer_s.AddActor(actor_t)
        renderer_t.AddActor(actor_t)




        # Iterative Closest Point transformation
        icpt = vtk.vtkIterativeClosestPointTransform()
        icpt.SetSource(data_s)
        icpt.SetTarget(data_t)
        icpt.GetLandmarkTransform().SetModeToRigidBody()
        icpt.SetMaximumNumberOfIterations(iteration)
        icpt.SetMaximumNumberOfLandmarks(landmark)

        # Measuring algorithm time
        start = process_time()
        icpt.Update()
        end = process_time()
        icp_time = (end - start) / 1000

        # Transformation
        tf_filter =vtk.vtkTransformPolyDataFilter()
        tf_filter.SetInputData(data_s)
        tf_filter.SetTransform(icpt)
        tf_filter.Update()

        tf_mapper = vtk.vtkPolyDataMapper()
        tf_mapper.SetInputConnection(tf_filter.GetOutputPort())

        tf_actor = vtk.vtkActor()
        tf_actor.SetMapper(tf_mapper);
        tf_actor.GetProperty().SetColor(0, 1, 0)
        renderer_t.AddActor(tf_actor)

        tf_data = tf_filter.GetOutput().GetPoints().GetData()
        t_data = data_t.GetPoints().GetData()

        sum_sq = 0
        d_sq = 0
        tf_x = 0
        t_x = 0
        tf_y = 0
        t_y = 0
        tf_z = 0
        t_z = 0

        for idx in range (tf_data.GetNumberOfTuples()):
            tf_x = tf_data.GetTuple3(idx)[0]
            tf_y = tf_data.GetTuple3(idx)[1]
            tf_z = tf_data.GetTuple3(idx)[2]
            t_x = t_data.GetTuple3(idx)[0]
            t_y = t_data.GetTuple3(idx)[1]
            t_z = t_data.GetTuple3(idx)[2]

            d_sq = (tf_x - t_x)**2 + (tf_y - t_y)**2 + (tf_z - t_z)**2
            sum_sq += d_sq

        error = sum_sq / tf_data.GetNumberOfTuples()

        print("Iterations: " + str(iteration) + "  Landmarks: " + str(landmark) + "  Error: " + str(error) + "  Time: " + str(icp_time) + "ms")

        # Showing results

        window_t.Render()
        window_t.SetWindowName("TargetPicture_" + str(n) + " It: " + str(iteration) + " Lm: " + str(landmark))
        if first:
            window_s.Render()
            window_s.SetWindowName("SourcePicture_" + str(n))
            window_s_interactor.Start()
            window_t_interactor.Start()

        else:
            window_t_interactor.Start()

        first = False




































