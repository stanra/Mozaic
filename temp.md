Around a month ago, we had the company strategic meeting. I only attended the R&D part of the meetings. It was for me the occasion to really understand what each team has been working on in the past, and what are they going to do in the near/medium future. We were also able to discuss some issues about the software part of the project, but this was less fruitful.
Here are some of my notes taken during this meeting.


This strategic meeting is there to start seriously planning future developments in the next 1-3 years, which are important, as we will start releasing our product and go on to future developments/improvements


# Instrument & Automatic Software

PD1 had a issue with a SiPM module. PD2's module are ok (but there are other issues).
The module is the first one to fail in 16. Hard to tell whether it is relevant or not.
Daniel is asking about some kind of unit tests for the module. Indeed, 'incoming QC' should do some acceptance tests. But Wistron isn't doing it (and they don't know how to, it'll be our job to plan it for them...)
Looking for secondary vendors for all the modules is important ! A secondary constructor instead of Winstron may be a good thing as well (as Wistron seems voluntarily unprofessional).

The instrument team still has some few bugs left, and software issues, but their project is well advanced. In the next few months, they are in a hurry to get the documentation for the GMP.
They are now actively thinking about future projects, such as : construction in house, new (lighter, more efficient) instrument, using our own software.  

# Software

This part is of course the most interesting for me, but there was nothing much new.


DAPI has a high cell to cell variation. But average should be somewhat stable over experiments. Therefore, it might be an idea to use it to *normalize* other channels (and also use it for handling 'contrast enhancement'). This needs to be thoroughly analyzed. If variability is dependent on cells, it won't be useful, but if the machine introduce variability, then using DAPI normalization may make all experiments more *comparable*.

Globally, *color ratios* should give useful information.


We discussed a bit about the planning with Neil, but recent changes following the strategic meeting made most of this conversation irrelevant now.
Note : I don't agree much with Neil – and this is normal and may be constructive – but I think the current situation between Cong-Xin and Neil prevents us from making real planning decisions (or any kind of similar decisions). All we can do is to try to extrapolate the information randomly given by Neil during the fights with Cong-Xin. In the future, I will probably take these conversations in my hands and try to have constructive conversations and decisions made.


According to Neil, Labs usually have their own software – or buy one – for detecting CTCs. This is why the software is not completely essential if the pictures can be exported (it just won't be that simple in real life for us!). We actually can consider these software as our "concurrents".


The Data Analysis may really be a future very strong point of our Software.
There are indeed many possibilities : beside image algorithm improvement and target cell detection, it can also be used for the troubleshooter, and for internal optimization of the instrument.
A powerful general CTC/target cell detection tool (better than linear filters) may also help having a globally better software.


Different collaborations with other teams were discussed :  
The bio group understands what we need from them for the reviewer.
The Instrument team mentioned the better handling of Data as one of their soon future task.
However, both teams are quite busy for the next few weeks, possibly until the end of the year.

# Biology

This part is not directly useful for me, but is very interesting and helps gets better perspective of our instrument.

Note : Globally, the bio group's work (especially JuYu's) really seems like they are trying to 'pioneer' the research that our instrument allows. It is interesting for the marketing of our product.

Just the biomarkers will cost at least $80/kit. If we add the price of a chip, one experiment will be quite expensive for the patient. This was maybe to be expected.


Our instrument is far from being only useful for CTC. CTC is the most important for clinical utility for now, but other applications of rare cell detection is very useful for research as well :

* Tumor reactive T-cells are very interesting in fighting cancer : they are a natural defense against cancer produced by the human.
If we are able to detect them, it may be very useful. Lots of recent research try to focus on that, and our instrument will really help that. These cells are indeed too rare for flow cytometry to be a practical solution.   

* Fetal cell is another 'new research field' that our instrument can help. We can indeed detect the baby's blood cell in the pregnant mom's blood. This is very useful for two quite different things :
        * Baby diagnosis : the cells help us diagnose many kind of disease (especially if we can get the DNA) of the baby in a non-invasive way.
        * placenta health : Placenta health is not directly linked to baby's heath but may have important long term effect on the mother health. This is especially important in 3rd world countries, where smaller health issues are more 'important'.  



The false trigger issue is way more difficult to solve than I thought. It is indeed relative to very different factors, and some of them are more *nature bugs* than *instrument bugs*...
Some debris are fluorescent in SiPM channel. Some cells are "non-specific bindings", but since it is only some of them, it is not really "non-specific". We have no idea why the protein will bind with the markers. Could be *endocytose* or other similar issues.

# Fludic Control

They need to precisely plan the factory, even though it is small and in house.  

The chip material costs ~$5, but it will be ~5x more with manufacturing process.
MiFluo materials cost ~$2/3  

Now, the chip and the process for the chip is more or less finished.

Beside figuring out the factory, they also work on QC and on improving the chip.
For the QC, since it's a 'critical' piece, they need to QC on all chips, not just random sample.
They have a slightly high failure rate, mostly due to contamination.
They are therefore looking for solution to correct that :
Contamination --> change the working plan material
Glass breaks when handling -> change the case to avoid having the glass come out of it (but they actively decided not to in the past, not sure it will be ok)


Another of their project is "research". They want to do sequential sorting on the chip.  
Our instrument has the ability to serve different purpose using the same machine, but different chip (and hardware).
This can be used to directly get the cells without filter and images or to have a different sorting system.
They make one to sort twice, without having to manually re-input the blood. Between the two sorting, there is a "dilution" (in space, not in volume. ''flow stretching'' might be a better term)
Techniques for that are *Tesla micromixer* and *Taylor dispersion*.

Taking the false triggers into account, our current purity should be around ~0.3%. With double sort and good enough dilution, we can go up to 6% (or actually 30% since false triggers may not be cell induced). Above 15% seems to be a good selling arguments, as is allows to use cheaper DNA analysis technologies.  
These numbers consider that we have 100% recovery, or that recovery is not affected by the second sort at least (which may be reasonable).


The other work seemed less important, but may actually be an awesome solution for future improvements of any kind if the early results are verified.  
One of the problem now is that the sorting makes more volume go into the blood after the sorting. Therefore pressure and flow rate increase quite a lot. This is an issue for sequential sorting for example.
Jeff tried a new solution to make this volume almost inexistant. I don't understand the solution (seems like it is using air or higher pressure lower volume), and Perry and Daniel don’t believe it works. If it does, it will make future ships a lot better so it should be a priority to continue these research.
